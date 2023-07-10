import sys
sys.path.append('project/chatbot_wenxin')


from config import cfg


llm_model_dict = cfg.readValue("basic", "llm_model_dict")
knowadge_index_dict = cfg.readValue("basic", "knowadge_index_dict")
embedding_model_dict = cfg.readValue("basic", "embedding_model_dict")


knowadge_choices = list(knowadge_index_dict.keys())
embedding_choices=list(embedding_model_dict.keys())
print(knowadge_choices)
print(embedding_choices)