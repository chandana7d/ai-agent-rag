from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Any
from langchain.schema import Document


@dataclass
class Config : 
    QUERY_TRANSLATOR = "simple"
    CHROMA_STORAGE   = "../db_data/chorma_langchain_db"
    COLLECTION_NAME  = "duplocloud"
    EMBEDDING_MODEL  = "text-embedding-3-large"
    
@dataclass
class urls:
    GITURL = "https://github.com/duplocloud/docs/tree/main/getting-started-1/application-focussed-interface"


@dataclass
class Query:
    data : str 


@dataclass
class GithubMeta:
    name : str 
    path : str 
    sha : str 
    size : str 
    url :  str 
    html_url : str 
    git_url : str 
    download_url : str 
    type : str 
    _links : Dict[str, str]

    def to_dict(self) -> Dict[str, any]:
        return asdict(self)

@dataclass
class GithubData:
    meta : GithubMeta
    data : str 
  
@dataclass 
class Chunk : 
    data : str 
    meta : GithubMeta


@dataclass
class SingleQuery:
    query          : str 
    is_modified    : Optional[bool] = None 
    updated_query  : Optional[str] = None

@dataclass
class MultiQuery:
    query : str
    querylist : List[str]

@dataclass
class UserQuery:
    query : SingleQuery | MultiQuery


# query translator prompts 
@dataclass
class QueryPrompts:

    SIMPLE_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
    )

    ENHANCER_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
        "Your goal is to generate multiple alternative queries that are more specific, detailed, or phrased differently "
        "to improve the chances of retrieving relevant documents from a vector database. "
        "Provide these alternative questions in a paragaraph Original question:  question: {question}" 
         "Output:" 
    )

    DECOMPOSITION_TEMPLATE: str = (
        "You are a helpful assistant that generates multiple sub-questions related to an input question. "
        "The goal is to break down the input into a set of sub-problems / sub-questions that can be answered in isolation. "
        "Generate multiple search queries related to: {question} \n"
        "Output (5 queries):"
    )


@dataclass 
class Context:
    is_vectordb: bool = False
    is_tool: bool = False
    docs : Optional[List[Document]] = None 
    tool_out : Optional[str] = None 
    query  : str  = None 