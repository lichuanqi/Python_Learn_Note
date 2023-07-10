import sys
import time
from datetime import datetime
import requests
import json

from config import cfg


CLIENT_ID = cfg.readValue('API_BAIDU', 'CLIENT_ID')
CLIENT_SECRET = cfg.readValue('API_BAIDU', 'CLIENT_SECRET')
ACCESS_TIME = datetime.strptime(cfg.readValue('API_BAIDU', 'ACCESS_TIME'), '%Y-%m-%d %H:%M:%S')
ACCESS_TOKEN = cfg.readValue('API_BAIDU', 'ACCESS_TOKEN')


def get_access_token():
    """根据API Key、Secret Key换取access_token"""
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&" \
          "client_id=%s&client_secret=%s"%(CLIENT_ID, CLIENT_SECRET)

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    access_time = datetime.now()
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    access_token = response_json["access_token"]

    return access_time, access_token


def update_access_token():
    """更新access_token"""
    global ACCESS_TIME
    global ACCESS_TOKEN

    if not isinstance(ACCESS_TIME, datetime):
        ACCESS_TIME = datetime(2023,1,1)
    if (datetime.now()-ACCESS_TIME).days <= 20:
        print('Token无需更新')
        return 

    access_time, access_token = get_access_token()
    if access_token is None:
        print('Token返回值为空')
        return 
    
    ACCESS_TIME, ACCESS_TOKEN = access_time, access_token
    cfg.setValue('API_BAIDU', 'ACCESS_TIME', ACCESS_TIME)
    cfg.setValue('API_BAIDU', 'ACCESS_TOKEN', ACCESS_TOKEN)
    print('初始化完成, access_token已更新')

    return 


def chat_by_token(message, stream=False):
    """根据access_token进行对话

    Params
        token: str 
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
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?"\
          "access_token=%s"%ACCESS_TOKEN
    
    payload = json.dumps({
        "messages": message,
        "stream": stream
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    return response_json


def run_in_terminal():
    """在终端实现对话"""
    update_access_token()
    messages = []
    
    while True:
        msg = input("输入: ")

        # 输入s退出
        if msg == "s":
            break

        messages.append({"role": "user","content": msg})
        reponse = chat_by_token(messages, stream=False)

        # 判断错误
        if "error_code" in reponse:
            print(reponse["error_msg"])

        # 返回字符串结果
        result = reponse["result"]
        # 统计tokens数
        prompt_tokens, completion_tokens = reponse["usage"]["prompt_tokens"], reponse["usage"]["completion_tokens"]

        messages.append({"role": "assistant","content": result})

        print('输出: %s'%result)
        print('统计: 问题tokens数%s, 回答tokens数%s'%(prompt_tokens, completion_tokens))
        print('\n')

if __name__ == '__main__':
    run_in_terminal()