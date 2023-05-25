import gradio as gr
import random
import time

from util import wenxin_to_chatbot, chatbot_to_wenxin
from api import ACCESS_TIME, ACCESS_TOKEN
from api import update_access_token, chat_by_token


def predict_base(message, chatbot, history:list=[]):
    """文本生成主函数, 主要用户调试每次都返回固定的字符串
    
    Params
        message: 输入
        history: 

    Return
        response: 对应于所有用户和机器人响应的字符串元组列表。
                  这将在 Gradio 演示中呈现为输出。
        history: 所有用户和机器人响应的令牌表示。
                 在有状态的 Gradio 演示中，我们必须在函数结束时返回更新的状态。
    """
    history.append({"role": "user", "content": message})
    response = "你好你好"
    history.append({"role": "assistant", "content": response})
    
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]

    return "", messages, history


def predict_wenxin(message, chatbot):
    """文本生成主函数, 调用文心一言接口"""
    access_time, access_token = update_access_token(ACCESS_TIME, ACCESS_TOKEN)

    history = chatbot_to_wenxin(chatbot)
    history.append({"role": "user","content": message})
    reponse = chat_by_token(access_token, history, stream=False)

    # 字符串结果
    result = reponse["result"]
    # tokens数
    prompt_tokens, completion_tokens = reponse["usage"]["prompt_tokens"], reponse["usage"]["completion_tokens"]

    history.append({"role": "assistant","content": result})
    messages = wenxin_to_chatbot(history)

    return "", messages


def on_clear():
    print('已清空历史消息')
    return [], None


with gr.Blocks(
    title="LLM",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown(
        """
        ## 🚀LLM助手
        使用文心一言商用API实现的大语言模型助手        
        """
    )
    history = []
    state = gr.State([])
    chatbot = gr.Chatbot().style(height=450)
    msg = gr.Textbox(
        label="Chat Message Box",
        placeholder="请输入要提问的问题",
        show_label=False,
    ).style(container=False)
    
    with gr.Column():
        with gr.Row():
            submit = gr.Button("Submit")
            stop = gr.Button("Stop")
            clear = gr.Button("Clear")

    # 输入框回车槽函数
    msg_event = msg.submit(
        fn=predict_wenxin,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
        queue=True,
    )
    # 提交按钮槽函数
    submit_event = submit.click(
        fn=predict_wenxin,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
        queue=True,
    )
    # 停止按钮槽函数
    stop.click(
        fn=None,
        inputs=None,
        outputs=None,
        cancels=[msg_event, submit_event],
        queue=False,
    )
    # 清空按钮槽函数
    clear.click(
        fn=on_clear,
        inputs=None,
        outputs=[state, chatbot],
        queue=False,
    )

demo.queue(max_size=16,
           concurrency_count=2)
demo.launch(share=False, 
            debug=False, 
            enable_queue=True)