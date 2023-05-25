def chatbot_to_wenxin(history:list):
    """
    chatbot格式
    [
        ["请介绍一下你自己", "百度公司开发的人工智能语言模型"],
        [..., ...]
    ]
    文心格式
    [
        {"role":"user","content":"请介绍一下你自己"},
        {"role":"assistant","content":"我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"},
        {"role":"user","content": "我在上海，周末可以去哪里玩？"}
    ]
    """
    wenxin = []
    for i in range(0, len(history)):
        wenxin.append({"role": "user","content": history[i][0]})
        wenxin.append({"role": "assistant","content": history[i][1]})

    return wenxin


def wenxin_to_chatbot(history:list):
    chatbot = [(history[i]["content"], history[i+1]["content"]) \
               for i in range(0, len(history)-1, 2)
    ]
    return chatbot