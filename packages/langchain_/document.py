from pprint import pprint
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2":"uer/sbert-base-chinese-nli",
    "text2vec3":"packages/langchain_/models/shibing624_text2vec-base-chinese",
}
persist_directory = 'packages/langchain_/vectordb'
file_path = 'packages/langchain_/test.txt'

# document load and split
loader = TextLoader(file_path=file_path, encoding='utf-8')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
doc_texts = loader.load_and_split(text_splitter=text_splitter)

# document Vector
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict["text2vec3"])
vectordb = Chroma.from_documents(documents=doc_texts, 
                                  embedding=embeddings,
                                  persist_directory=persist_directory)

# vector store
vectordb.persist()

# Vector search
query = "中央主题教育工作会议什么时候召开的"
docs = vectordb.similarity_search(query)

pprint(docs)