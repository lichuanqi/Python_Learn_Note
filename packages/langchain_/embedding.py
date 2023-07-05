import sys
from datetime import datetime
from pathlib import Path
from pprint import pprint
from dataclasses import dataclass, field

import pandas as pd
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


@dataclass
class DataItem:
    file_name: str=''
    file_path: str=''
    file_hash: str=''
    doc_ids: list=field(default_factory=list)
    add_time: str=''


class DataList():
    """弥补向量数据库无法实现保存文档基础信息的功能"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.read()
        
    def read(self):
        if Path(self.filepath).exists():
            self.dataframe = pd.read_csv(
                filepath_or_buffer=self.filepath, 
                index_col=0, 
                header=0,
                encoding='utf-8')
            print('共读取 %s 条数据'%len(self.dataframe.index))
        else:
            columns = DataItem().__dict__.keys()
            self.dataframe = pd.DataFrame(columns=columns)
            print('路径不存在已新建')

    def add(self, _data: DataItem):
        """增加一条数据"""
        if not self.search(_data.file_name):
            data_dict = _data.__dict__
            self.dataframe = self.dataframe._append(data_dict, ignore_index=True)
            self.updateFile()
            print('数据插入成功')
        else:
            print('数据已存在插入失败')

    def delete_one(self, file_name):
        """删除一条数据"""
        if not self.search(file_name):
            print('数据不存在')
        else:
            pass

    def search(self, file_name) -> bool:
        """根据文件名判断是否已存在"""
        if file_name in self.dataframe['file_name'].values:
            return True
        else:
            return False

    def updateFile(self):
        """文件修改后保存"""
        with open(self.filepath, 'w') as f:  
            self.dataframe.to_csv(path_or_buf=f, 
                             index=True,
                             lineterminator='\n',
                             encoding='utf-8')


def main():
    # 向量化模型
    embedding_model_dict = {
        "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
        "ernie-base": "nghuyong/ernie-3.0-base-zh",
        "text2vec": "GanymedeNil/text2vec-large-chinese",
        "text2vec2":"uer/sbert-base-chinese-nli",
        "text2vec3":"packages/langchain_/models/shibing624_text2vec-base-chinese",
        "m3e-small": "packages/langchain_/models/moka-ai_m3e-small"
    }
    # 向量数据保存路径
    persist_directory = 'packages/langchain_/vectordb'

    # 保存文档列表
    filelist_path = 'packages/langchain_/vectordb/filelist.csv'
    if Path(filelist_path).exists():
        filelist = pd.read_csv(filelist_path)
    else:
        columns = ['file_name', 'file_path', 'file_hash', 'file_id', 'add_time']
        filelist = pd.DataFrame(columns=columns)

    # document Vector
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict["m3e-small"])

    if Path(persist_directory).exists():
        print('向量数据保存目录存在, 从路径加载向量数据库')
    else:
        print('向量数据保存目录不存在, 新建空的向量数据库')
    vectordb = Chroma(embedding_function=embeddings,
                    persist_directory=persist_directory)

    # 判断文档是否已经保存过
    file_path = 'packages/langchain_/test.txt'
    file_name = Path(file_path).name
    print(file_path)
    if file_path not in filelist['file_name'].values:
        print('√ 文档未在列表中开始读取增加、切分、保存: %s'%file_name)
        loader = TextLoader(file_path=file_path, encoding='utf-8')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
        doc_texts = loader.load_and_split(text_splitter=text_splitter)
        docids = vectordb.add_documents(documents=doc_texts)
        vectordb.persist()
        print('√ 文档信息保存至csv')

        _file = {'file_name': file_name,
                'file_path': file_path, 
                'file_hash': 'hash',
                'doc_ids': docids,
                'add_time': datetime.now()}
        filelist = filelist._append(_file, ignore_index=True)
        filelist.to_csv(filelist_path)
        print('√ 文档信息保存至csv')

    else:
        print('x 文档已存在跳过数据持久化')

    print('向量检索')
    query = "用2-3句话解释一下寄递市场库"
    docs = vectordb.similarity_search_with_score(query)
    print('检索问题: %s'%query)
    pprint('检索结果: \n%s'%docs)

def test_datalist():
    datapath = 'packages/langchain_/vectordb/filelist_test.csv'
    data = DataItem(file_name='name003',
                    file_hash='/name.txt',
                    file_path='hash',
                    doc_ids=['a','b'],
                    add_time=datetime.now())
    datalist = DataList(datapath)
    datalist.add(data)


if __name__ == '__main__':
    test_datalist()