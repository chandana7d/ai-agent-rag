
import os
from dataclasses import dataclass,asdict
import requests
import json 
from typing import Dict, Optional, List, Tuple,Iterator
from langchain_chroma import Chroma
from langchain_openai  import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_core.vectorstores.base import VectorStore
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Callable
from config import *

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


class GitHubCrawler:
    def download_meta(self, url : str) -> Iterator[GithubMeta]:
        _, _, _, owner, repo, tree, branch, *path_parts = url.split('/')
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{'/'.join(path_parts)}?ref={branch}"
        meta_data : GithubMeta = self._meta_data(api_url)
        list_meta = []
        for item in meta_data:
            if item.type == 'dir':
                list_meta += self.download_meta(item.html_url)
            else:
                list_meta += [item]
        return list_meta 
    
    def invoke(self):
        list_meta : Iterator[GithubMeta] = self.download_meta(url = urls.GITURL)        
        data      : Iterator[Optional[GithubData]] = [self.download_data(meta_data) for meta_data in list_meta]

        return data 

    
    def download_data(self, meta_data : GithubMeta) -> Optional[GithubData] :
        download_url  = meta_data.download_url
        file_response = requests.get(download_url)
        if file_response.status_code == 200:
            # Chunk the document content
            raw_text = file_response.text
            return GithubData( meta=meta_data, data=raw_text)

        else:
            print(f"Failed to download {meta_data.name}. Status code: {file_response.status_code}")
            return None 


    def _meta_data(self, api_url) -> Iterator[Optional[GithubMeta]]:
        response = requests.get(api_url)
        if response.status_code == 200:
            json_out  = json.loads(response.text)
            return [GithubMeta(**json_obj) for json_obj in json_out]
        else:
            return [] 
        












    
    






