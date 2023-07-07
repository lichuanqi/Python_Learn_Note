# -*- coding: utf-8 -*-
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
from langchain.chains.combine_documents.base import (
    BaseCombineDocumentsChain,
    format_document)
from langchain import PromptTemplate

from config import cfg


@dataclass
class DocumentListItem():
    file_name: str=''
    file_path: str=''
    file_hash: str=''
    doc_ids: list=field(default_factory=list)
    add_time: str=''


class DocumentListData():
    """本地知识库文档列表数据
    
    弥补向量数据库无法实现保存文档基础信息的功能
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.read()
        
    def read(self):
        if Path(self.filepath).exists():
            self.dataframe = pd.read_csv(
                filepath_or_buffer=self.filepath, 
                index_col=0, 
                header=0,
                encoding='GB18030')
            print('共读取 %s 条数据'%len(self.dataframe.index))
        else:
            columns = DocumentListItem().__dict__.keys()
            self.dataframe = pd.DataFrame(columns=columns)
            self.updateFile()
            print('路径不存在已新建')

    def add(self, _data: DocumentListItem):
        """增加一条数据"""
        if not self.search(_data.file_name):
            data_dict = _data.__dict__
            self.dataframe = self.dataframe._append(data_dict, ignore_index=True)
            self.updateFile()
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
            self.dataframe.to_csv(
                path_or_buf=f, 
                index=True,
                lineterminator='\n',
                encoding='GB18030')


class DocumentVectorData():        
    """本地知识库向量数据"""
    def __init__(self,
                 embedding_model_name,
                 data_dir) -> None:
        """
        Params
            embedding_model_name
            list_path
            vector_dir
        """
        list_path = Path(data_dir) / 'filelist.csv'
        vector_dir = Path(data_dir) / 'vectordb'
        file_dir = Path(data_dir) / 'filedata'

        self.documentListData = DocumentListData(list_path)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vectordb = Chroma(
            embedding_function=self.embeddings,
            persist_directory=str(vector_dir))
        
    def add_file(self, filepath):
        """增加新的文档"""
        # 判断文件是否存在
        if not Path(filepath).exists():
            print('文件不存在已跳过')
            return 
        file_name = Path(filepath).name
        print('开始处理: %s'%file_name)

        # 判断文件是否已经保存过
        if self.documentListData.search(file_name):
            print('x 文档已存在跳过数据持久化')
            return 
        
        # 判断文件类型
        if Path(filepath).suffix != '.txt':
            print('目前无法处理此类型文件', Path(filepath).suffix)
            return
        
        print('√ 文档未在列表中开始读取增加、切分、保存: %s'%file_name)
        loader = TextLoader(file_path=filepath, encoding='utf-8')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        doc_texts = loader.load_and_split(text_splitter=text_splitter)
        docids = self.vectordb.add_documents(documents=doc_texts)
        self.vectordb.persist()
        print('√ 保存向量数据库')

        _file = DocumentListItem(
            file_name=file_name,
            file_path=filepath,
            file_hash='hash',
            doc_ids=docids,
            add_time=datetime.now()
        )
        self.documentListData.add(_file)
        print('√ 文档信息保存至csv')

    def similarity_search(self, question:str):
        vectordb_search = self.vectordb.similarity_search(question)
        return vectordb_search


embedding_model_dict = cfg.readValue('basic', 'embedding_model_dict')
data_dir = cfg.readValue('basic', 'datadir')


documentVectorData =DocumentVectorData(
    embedding_model_name=embedding_model_dict["text2vec3"],
    data_dir=data_dir) 


def test_document_data():
    # 增加文档
    file = "D:/CPRI/01_规章制度/食住行/邮政科学研究规划院在职无房职工住房补贴.txt"
    documentVectorData.add_file(file)

    # 检索
    question = "我是一名新入职的员工我能拿多少住房补贴"
    vectordb_search = documentVectorData.similarity_search(question)

    # 拼接检索内容
    document_prompt = PromptTemplate(
        input_variables=["page_content"], 
        template="{page_content}")
    doc_strings = [format_document(doc, document_prompt) for doc in vectordb_search]
    # print(doc_strings)

    # 拼接大语言模型输入信息
    chat_template = """基于以下已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分。
    已知网络检索内容：{web_content}
    已知内容: {context}
    问题: {question}
    """
    chat_prompt= PromptTemplate(
        input_variables=["web_content", "context", "question"], 
        template=chat_template)
    chat_strings = chat_prompt.format(
        web_content='无', 
        context=doc_strings, 
        question=question)
    print(chat_strings)


if __name__ == '__main__':
    test_document_data()