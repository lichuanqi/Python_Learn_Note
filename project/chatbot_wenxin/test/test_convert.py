"""测试chatbot格式和文心格式之间的转换"""
import sys
sys.path.append('project/chatbot_wenxin')

from util import wenxin_to_chatbot, chatbot_to_wenxin


wenxin = [
        {"role":"user","content":"请介绍一下你自己"},
        {"role":"assistant","content":"我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"},
        {"role":"user","content": "我在上海，周末可以去哪里玩？"}
]
chatbot = [
        ["请介绍一下你自己", "百度公司开发的人工智能语言模型"],
        ["你好", "你也好"]
]

chatbot_new = wenxin_to_chatbot(wenxin)
print(chatbot_new)

wenxin_new = chatbot_to_wenxin(chatbot)
print(wenxin_new)