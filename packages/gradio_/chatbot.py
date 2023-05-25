import gradio as gr
import random
import time


def generate(message, history: list=[]):
    """文本生成主函数
    
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

    return messages, history


with gr.Blocks(
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown(
        """
        ## 🚀LLM助手
        使用文心一言商用API实现的大语言模型助手        
        """
    )

    chatbot = gr.Chatbot().style(height=450)
    state = gr.State([])
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

    submit_event = submit.click(
        fn=generate,
        inputs=[msg, state],
        outputs=[chatbot, state],
        queue=True,
    )
    stop.click(
        fn=None,
        inputs=None,
        outputs=None,
        cancels=[submit_event],
        queue=False,
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue(max_size=16,
           concurrency_count=2)
demo.launch(share=False, 
            debug=False, 
            enable_queue=True)