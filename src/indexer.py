import os
from dataclasses import dataclass,asdict
import requests
import json 
from typing import Dict, Optional, List, Tuple,Iterator
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_core.vectorstores.base import VectorStore
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Callable
from config import *

class ChromaVectorStore:

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.presist_dir = Config.CHROMA_STORAGE
        self.chroma_db = Chroma(embedding_function=self.embeddings,persist_directory=self.presist_dir)

    def get_vectorstore(self, collection : str = "duplocloud")-> Optional[VectorStore]:
        if self._check_collection_exist(collection):
            return Chroma(embedding_function=self.embeddings,persist_directory=self.presist_dir, collection_name=collection)
        else: 
            return None    
    
    def _check_collection_exist(self,collection)->bool:
        collection_list = self.chroma_db._client.list_collections() 
        collection_names = [col.name for col in collection_list]
        if collection in collection_names:
            return True
        else:
            return False


class DocumentIndexer:
    def __init__(self):
        self.chunk_size     : int     = 1000
        self.chunk_overlap  : int     = 100
        self.COLLECTION_NAME : str    = Config.COLLECTION_NAME
        self.PRESISTENT_DIR  : str    = Config.CHROMA_STORAGE

        self.embeddings     : OpenAIEmbeddings  = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vector_store   : VectorStore       = Chroma(
                                                collection_name=self.COLLECTION_NAME,
                                                  embedding_function=self.embeddings,
                                                  persist_directory= self.PRESISTENT_DIR)

    def invoke(self, docs :  List[GithubData]) -> VectorStore:
        for doc in docs:
            chuncks = self._chunk(doc) 
            self._index(chunks=chuncks)
        
        print(self.vector_store._client.list_collections())
        return self.vector_store
    

    def _check_doc_directory_persists(self) -> bool:
        if os.path.exists(self.PRESISTENT_DIR) and os.path.isdir(self.PRESISTENT_DIR):
            return True
        else:
            return False


    
    def _index(self, chunks : List[Chunk]):
        documents : List[Document] = [ Document(page_content=chunk.data, metadata=chunk.meta) for chunk in chunks]
        self.vector_store.add_documents(documents)
        
 
    def _chunk(self, document : GithubData ) -> List[Chunk]:
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        list_str = text_splitter.split_text(document.data)
        return [Chunk(data = str_chunk, meta= {"name" : document.meta.name}) for str_chunk in list_str]
    

