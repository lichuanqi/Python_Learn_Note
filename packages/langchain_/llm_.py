import os
from typing import Dict,List,Any,Optional,Tuple,Union,Mapping
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
import websocket
import requests

from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import cfg


BAIDU_CLIENT_ID = cfg.readValue('API_BAIDU', 'CLIENT_ID')
BAIDU_CLIENT_SECRET = cfg.readValue('API_BAIDU', 'CLIENT_SECRET')
BAIDU_ACCESS_TIME = cfg.readValue('API_BAIDU', 'ACCESS_TIME')
BAIDU_ACCESS_TOKEN = cfg.readValue('API_BAIDU', 'ACCESS_TOKEN')

SPARK_APPID = cfg.readValue('API_XUNFEI', 'appid')
SPARK_API_KEY = cfg.readValue('API_XUNFEI', 'api_key')
SPARK_API_SECRET = cfg.readValue('API_XUNFEI', 'api_secret')
result_list = []


class ExampleLLM(LLM):
    """封装语言模型类"""
    responses: List
    i: int = 0

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "fake-list"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """First try to lookup in queries, else return 'foo' or 'bar'."""
        response = self.responses[self.i]
        self.i += 1
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}


class ChatGlmLLM(LLM):
    max_token: int = 10000
    temperature: float = 0.1
    top_p = 0.9
    history = []
    tokenizer: object = None
    model: object = None

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "ChatLLM"

    def _call(self,
              prompt: str,
              stop: Optional[List[str]] = None) -> str:
        
        response = '你好啊'
        self.history.append((prompt, response))

        return response
    

class WenxinLLM(LLM):
    """百度文心一言"""

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "baidu-wenxin"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """First try to lookup in queries, else return 'foo' or 'bar'."""
        
        api_reponse = self.chat_by_token(prompt, stream=False)

        if "error_code" in api_reponse:
            response = api_reponse["error_msg"]
        else:
            response = api_reponse["result"]

        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}

    def get_access_token(self):
        """根据API Key、Secret Key换取access_token"""
            
        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&" \
              "client_id=%s&client_secret=%s"%(BAIDU_CLIENT_ID, BAIDU_CLIENT_SECRET)

        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'}
        
        access_time = datetime.now()
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        access_token = response_json["access_token"]

        return access_time, access_token

    def update_access_token(self):
        """更新access_token"""
        global BAIDU_ACCESS_TIME
        global BAIDU_ACCESS_TOKEN

        try:
            BAIDU_ACCESS_TIME = datetime.strptime(BAIDU_ACCESS_TIME, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            BAIDU_ACCESS_TIME = datetime(2023,1,1)
        
        if (datetime.now()-BAIDU_ACCESS_TIME).days <= 20:
            print('Token无需更新')
            return 

        access_time, access_token = self.get_access_token()
        if access_token is None:
            print('Token返回值为空')
            return
        
        BAIDU_ACCESS_TIME, BAIDU_ACCESS_TOKEN = access_time, access_token
        cfg.setValue('API_BAIDU', 'ACCESS_TIME', BAIDU_ACCESS_TIME)
        cfg.setValue('API_BAIDU', 'ACCESS_TOKEN', BAIDU_ACCESS_TOKEN)
        print('初始化完成, access_token已更新')

        return
    
    def chat_by_token(self, message:list, stream=False):
        """根据access_token进行对话

        Params
            message: list 聊天上下文信息
                    (1)messages成员不能为空;1个成员表示单轮对话,多个成员表示多轮对话。
                    (2)最后一个message为当前请求的信息,前面的message为历史对话信息。
                    (3)必须为奇数个成员,成员中message的role必须依次为user、assistant。
                    (4)最后一个message的content长度(即此轮对话的问题)不能超过2000个字符;
                    如果messages中content总长度大于2000字符,系统会依次遗忘最早的历史会话,直到content的总长度不超过2000个字符。

                    单轮请求示例
                    [
                        {"role":"user","content":"介绍一下你自己"}
                    ]
                    多轮请求示例
                    [
                        {"role":"user","content":"请介绍一下你自己"},
                        {"role":"assistant","content":"我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"},
                        {"role":"user","content": "我在上海，周末可以去哪里玩？"}
                    ]
            
            stream: bool 是否以流式接口的形式返回数据,默认false。
            user_id: str 最终用户的唯一标识符，可以监视和检测滥用行为，防止接口恶意调用。

        Return
            id: string 本轮对话的id。
            object: string 回包类型。
                    chat.completion 多轮对话返回
            created: int 时间戳。
            sentence_id: int 表示当前子句的序号。只有在流式接口模式下会返回该字段。
            is_end: bool 表示当前子句是否是最后一句。只有在流式接口模式下会返回该字段。
            result: string 对话返回结果。
            need_clear_history: bool 表示用户输入是否存在安全，是否关闭当前会话，清理历史回话信息。
                                true表示用户输入存在安全风险,建议关闭当前会话,清理历史会话信息。
                                false:否,表示用户输入无安全风险。
            usage: token统计信息,token数 = 汉字数+单词数*1.3 （仅为估算逻辑）。
                prompt_tokens-问题tokens数,completion_tokens-回答tokens数,total_tokens-tokens总数。
        """
        self.update_access_token()

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?" \
              "access_token=%s"%BAIDU_ACCESS_TOKEN
        payload = json.dumps({
            "messages": message,
            "stream": stream})
        headers = {'Content-Type': 'application/json'}
        
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        return response_json


class XinghuoLLM(LLM):
    """讯飞星火"""
    gpt_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # spark官方模型提供api接口
    host = urlparse(gpt_url).netloc  # host目标机器解析
    path = urlparse(gpt_url).path  # 路径目标解析
    max_tokens = 1024
    temperature = 0.5
 
    # ws = websocket.WebSocketApp(url='')
 
    @property
    def _llm_type(self) -> str:
        # 模型简介
        return "Spark"
 
    def _get_url(self):
        # 获取请求路径
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
 
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"
 
        signature_sha = hmac.new(SPARK_API_SECRET.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
 
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
 
        authorization_origin = f'api_key="{SPARK_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
 
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
 
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.gpt_url + '?' + urlencode(v)
        return url
 
    def _post(self, prompt):
        #模型请求响应
        websocket.enableTrace(False)
        wsUrl = self._get_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error,
                                    on_close=on_close, on_open=on_open)
        ws.question = prompt
        setattr(ws, "temperature", self.temperature)
        setattr(ws, "max_tokens", self.max_tokens)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return ws.content if hasattr(ws, "content") else ""
 
    def _call(self, prompt: str,
              stop: Optional[List[str]] = None) -> str:
        # 启动关键的函数
        content = self._post(prompt)
        # content = "这是一个测试"
        return content
 
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get the identifying parameters.
        """
        _param_dict = {
            "url": self.gpt_url
        }
        return _param_dict
    

def _construct_query(prompt, temperature, max_tokens):
    data = {
        "header": {
            "app_id": SPARK_APPID,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": "general",
                "random_threshold": temperature,
                "max_tokens": max_tokens,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": prompt}
                ]
            }
        }
    }
    return data


def _run(ws, *args):
    data = json.dumps(
        _construct_query(prompt=ws.question, temperature=ws.temperature, max_tokens=ws.max_tokens))
    # print (data)
    ws.send(data)
 
 
def on_error(ws, error):
    print("error:", error)
 
 
def on_close(ws, a, b):
    print("closed...")
 
 
def on_open(ws):
    thread.start_new_thread(_run, (ws,))
 
 
def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    # print(data)
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        result_list.append(content)
        if status == 2:
            ws.close()
            setattr(ws, "content", "".join(result_list))
            print(result_list)
            result_list.clear()


def test_WenxinLLM():
    llm = WenxinLLM()
    question = [{"role": "user", "content": "介绍一下你自己"}]
    result = llm.chat_by_token(question)
    print(result)


def test_XinghuoLLM():
    llm = XinghuoLLM()
    question = [{"role":"user","content":"介绍一下你自己"}]
    result = llm(question, stop=["you"])
    print(result)


if __name__ == '__main__':
    # test_WenxinLLM()
    test_XinghuoLLM()