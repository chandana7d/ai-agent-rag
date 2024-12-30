import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from typing import List, Callable, Optional
from langchain.prompts import ChatPromptTemplate
from dataclasses import dataclass
from langchain.schema.agent import AgentFinish
from langchain_core.utils.function_calling import convert_to_openai_function
from dataclasses import dataclass
from typing import Optional
from langchain_core.vectorstores.base import VectorStore

#####
from config import *
from tools import get_current_weather, search_wikipedia, get_brave_online_search
from translator import UserQuery, SingleQuery, MultiQuery

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


TOOLS = [get_current_weather, search_wikipedia, get_brave_online_search]
FUNCTIONS = [convert_to_openai_function(f) for f in TOOLS]
TOOL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are provided with a list of tools and their description. Your job is to select one of them. If None Selected, use `get_brave_online_search` and generate structured output"),
    ("user", "{input}")
])

@dataclass
class RouterDecision:
    is_vectordb: bool = False
    is_tool: bool = False
    tool_name: Optional[str] = None
    tool_args: Optional[dict] = None
    query    : str = None 
    vector_store : Optional[VectorStore] =  None 


class ChromaDBChecker:
    def __init__(self, vectordb):
        self.vectordb = vectordb

    def check_query(self, query: str) -> tuple:
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=5)
        if docs_and_scores:
            scores = [score for _, score in docs_and_scores]
            avg_score = sum(scores) / len(scores)
            relevance_score = 1 - (avg_score / 2)
            if relevance_score > 0.5:
                return True
        return False
    
    def get_score(self, query: UserQuery)-> float:
        pass



class Tools:
    def __init__(self, tools: List[Callable] = None, llm : ChatOpenAI=None):
        self.tools       = [] if tools is None else tools 
        self.TOOL_PROMPT = TOOL_PROMPT
        self.llm         = ChatOpenAI(temperature=0) if llm is None else llm 
        self.llm         = self.register(tool=self.tools)

    def list_tools(self) -> Optional[List[Callable]]:
        return self.tools 

    def register(self, tool : List[Callable]) : 
        f = [convert_to_openai_function(tool) for tool in self.tools]
        return self.llm.bind(functions=f)


    def invoke(self, query : str):
        chain  = self.TOOL_PROMPT | self.llm | OpenAIFunctionsAgentOutputParser()
        result = chain.invoke({"input": query})
        if isinstance(result, AgentFinish):
            return result.return_values['output'], None
        else:
            tool_input = result.tool_input
            tool_name  = result.tool 

            return tool_name, tool_input



class QueryRouter: 
    def __init__(self, vector_store):
        self.vector_store    = vector_store
        self.chromadb_checker = ChromaDBChecker(vectordb = vector_store)
        self.tool  = Tools(tools = TOOLS)

    def invoke(self,query:UserQuery) -> RouterDecision:
        if isinstance(query,SingleQuery):  
            is_vectordb = self.chromadb_checker.check_query(query=query.query)
    
            if is_vectordb:
                return RouterDecision(is_vectordb=True,query=query.query, vector_store=self.vector_store)
            else: 
                print()
                tool_name, tool_input = self.tool.invoke(query=query.query)
                return RouterDecision(is_tool=True, tool_name=tool_name, tool_args=tool_input, query=query.query)
        
        #TODO -implement Mulitquery of the user this can come from query decomposition
        elif isinstance(query,MultiQuery):
            pass