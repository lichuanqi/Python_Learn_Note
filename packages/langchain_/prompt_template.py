from langchain import PromptTemplate


chat_template = """基于以下已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分。\
已知网络检索内容：{web_content}
已知内容: {context}
问题: {question}"""
chat_prompt = PromptTemplate(
    input_variables=["web_content", "context", "question"],
    template=chat_template,)
chat_strings = chat_prompt.format(
    web_content='网络检索内容', 
    context='已知内容', 
    question='问题')
print(chat_strings)