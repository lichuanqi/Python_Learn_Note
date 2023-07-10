import gradio as gr
import random
import time

from util import wenxin_to_chatbot, chatbot_to_wenxin
from api import update_access_token, chat_by_token
from config import cfg
from index_admin import documentVectorData,search_to_strings,message_to_input


llm_model_dict = cfg.readValue("basic", "llm_model_dict")
knowadge_index_dict = cfg.readValue("basic", "knowadge_index_dict")
embedding_model_dict = cfg.readValue("basic", "embedding_model_dict")

llm_choices = list(llm_model_dict.keys())
knowadge_choices = list(knowadge_index_dict.keys())
embedding_choices=list(embedding_model_dict.keys())


def request_api_base(message, chatbot):
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
    history = chatbot_to_wenxin(chatbot)
    history.append({"role": "user", "content": message})
    response = "你好你好"
    history.append({"role": "assistant", "content": response})
    
    messages = wenxin_to_chatbot(history)

    return "", messages


def request_api_wenxin(message, chatbot):
    """文本生成主函数, 调用文心一言接口"""
    update_access_token()

    history = chatbot_to_wenxin(chatbot)
    history.append({"role": "user","content": message})
    reponse = chat_by_token(history, stream=False)

    # 字符串结果
    result = reponse["result"]
    # tokens数
    prompt_tokens, completion_tokens = reponse["usage"]["prompt_tokens"], reponse["usage"]["completion_tokens"]

    history.append({"role": "assistant","content": result})
    messages = wenxin_to_chatbot(history)

    return "", messages


def onButtomSubmit(chat_mode, 
                   vector_search_top_k, 
                   history_len, 
                   temperature, 
                   top_p, 
                   question, 
                   history):
    """"提交按钮槽函数

    Params
        chat_mode        : 是否使用本地知识库
        vector_search_top_k : 向量数据库检索TOP K
        history_len,        : 最大对话轮数
        temperature, 
        top_p, 
        message
        chatbot
    
    Return
        message
        chatbot
    """
    history_wx = chatbot_to_wenxin(history)

    # 根据对话模型拼接用户输入
    if chat_mode == "本地知识库对话-test-index":
        vectordb_search = documentVectorData.similarity_search(question)
        doc_strings = search_to_strings(vectordb_search)
        content = message_to_input(question, doc_strings)
        print('本地知识库对话')
        
    elif chat_mode == "文档对话-不使用本地知识库":
        content = question
        print('文档对话')

    else:
        content = question
        print('通用对话')
    
    # 拼接历史对话
    history_wx.append({"role": "user","content": content})

    # 调用API接口
    update_access_token()
    reponse = chat_by_token(history_wx, stream=False)
    result = reponse["result"]
    
    # 统计tokens数
    prompt_tokens, completion_tokens = reponse["usage"]["prompt_tokens"], reponse["usage"]["completion_tokens"]
    history_wx.append({"role": "assistant","content": result})
    history_chatbot = wenxin_to_chatbot(history_wx)

    return "", history_chatbot


def onButtomClear():
    print('已清空历史消息')
    return [], None


def main():
    with gr.Blocks(title="LLM") as demo:
                #    theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
                    ## 🚀LLM助手
                    使用文心一言商用API实现的大语言模型助手        
                    """)
        history = []
        state = gr.State([])

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Accordion("对话模式"):
                    chat_mode = gr.Radio(
                        label="use knowadge",
                        choices=knowadge_choices,
                        value=knowadge_choices[0])
                    embedding_model = gr.Dropdown(
                        label="Embedding model",
                        choices=embedding_choices,
                        value=embedding_choices[0])
                    vector_search_top_k = gr.Slider(
                        1,
                        10,
                        value=6,
                        step=1,
                        label="vector search top k",
                        interactive=True)
                    # upload_file = gr.File(
                    #     label='增加知识库文件',
                    #     file_types=['.txt', '.md'])
                    
                with gr.Accordion("模型参数配置"):
                    large_language_model = gr.Dropdown(
                        choices=llm_choices,
                        label="large language model",
                        value=llm_choices[0])
                    history_len = gr.Slider(
                        0,
                        5,
                        value=3,
                        step=1,
                        label="history len",
                        interactive=True)
                    temperature = gr.Slider(
                        0,
                        1,
                        value=0.95,
                        step=0.01,
                        label="temperature",
                        interactive=True)
                    top_p = gr.Slider(
                        0,
                        1,
                        value=0.7,
                        step=0.1,
                        label="top_p",
                        interactive=True)

            with gr.Column(scale=4):
                chatbot = gr.Chatbot(height=480)

                with gr.Row():
                    msg = gr.Textbox(
                        label="Chat Message Box",
                        placeholder="请输入要提问的问题",
                        show_label=False,
                        container=False,
                        scale=5)
                    submit = gr.Button("Submit",scale=1)
                
                gr.Examples(
                    examples=[
                        "写一个大学生心理情景剧大赛的参赛剧本，描述大学生活中少年A从迷茫到找到奋斗方向的故事",
                        "帮我设计一个可以打出sin函数的代码",
                        "查一个知识："],
                    inputs=msg,
                    outputs=None,
                    cache_examples=False,
                    label="快速提问")

                with gr.Row():
                    stop = gr.Button("Stop")
                    clear = gr.Button("Clear")
        
        # 输入框回车槽函数
        msg_event = msg.submit(
            fn=onButtomSubmit,
            inputs=[chat_mode, vector_search_top_k, 
                    history_len, temperature, top_p, msg, chatbot],
            outputs=[msg, chatbot],
            queue=True)
        # 提交按钮槽函数
        submit_event = submit.click(
            fn=onButtomSubmit,
            inputs=[chat_mode, vector_search_top_k, 
                    history_len, temperature, top_p, msg, chatbot],
            outputs=[msg, chatbot],
            queue=True)
        # 停止按钮槽函数
        stop.click(
            fn=None,
            inputs=None,
            outputs=None,
            cancels=[msg_event, submit_event],
            queue=False)
        # 清空按钮槽函数
        clear.click(
            fn=onButtomClear,
            inputs=None,
            outputs=[state, chatbot],
            queue=False)

    demo.queue(max_size=16,
            concurrency_count=2)
    demo.launch(server_name="0.0.0.0",
                server_port=7860,
                show_error=True,
                share=False, 
                debug=False, 
                enable_queue=True)
    

if __name__ == '__main__':
    main()