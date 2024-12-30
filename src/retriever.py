#retriver class 
from langchain_chroma import Chroma
from typing import Dict, Optional, List, Tuple,Iterator, Any
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Callable
from langchain_core.vectorstores.base import VectorStore
from config import *
from translator import UserQuery, SingleQuery, MultiQuery
from tools import get_current_weather, search_wikipedia, get_brave_online_search
from router import RouterDecision


TOOL_MAP = {'get_current_weather':get_current_weather, 'search_wikipedia':search_wikipedia, "get_brave_online_search" : get_brave_online_search} 
from dataclasses import dataclass



class VectorDBQueryRetriver:

    def __init__(self,vector_store):
        self.vector_store : Chroma = vector_store

    def invoke(self, router_decision : RouterDecision):
        
        docs_w_score  : List[Tuple[Document, float]] = self.vector_store.similarity_search_with_score(query = router_decision.query ,k = 3)
        docs : List[Document]= [doc for doc, _ in docs_w_score]
        return Context(is_vectordb=router_decision.is_vectordb, docs=docs, query=router_decision.query)
        
    
 
class ToolQueryRetriever:
    def __init__(self):
        self.tool_map = TOOL_MAP

    def invoke(self, router_decision: RouterDecision) -> Optional[Context]:
        func_name = router_decision.tool_name           
        func = self.tool_map[func_name]
        args = router_decision.tool_args
        
        result = func(args)  
        return Context(is_tool=True, tool_out=result, query=router_decision.query)



class QueryRetriever:

    def invoke(self,router_decision : RouterDecision) -> Context :
        print(router_decision)

        if router_decision.is_tool:
            output : Context = ToolQueryRetriever().invoke(router_decision=router_decision)

        elif router_decision.is_vectordb:
            output : Context = VectorDBQueryRetriver(vector_store = router_decision.vector_store ).invoke(router_decision=router_decision)

        return output


