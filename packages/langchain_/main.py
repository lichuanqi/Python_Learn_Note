from langchain.embeddings import HuggingFaceEmbeddings


embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2":"uer/sbert-base-chinese-nli",
    "text2vec3":"shibing624/text2vec-base-chinese",
}

embeddings = HuggingFaceEmbeddings(model_name="packages\langchain_\models\shibing624_text2vec-base-chinese")
text = "今天几号"
query_result = embeddings.embed_query(text)
print(query_result)