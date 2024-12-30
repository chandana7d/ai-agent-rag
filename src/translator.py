import pandas as pd 
from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Optional, List
from dotenv import load_dotenv
from config import * 
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

#base query translator
class BaseQueryTranslator:
    def __init__(self):
        pass 

    def invoke(self,query):
        raise NotImplementedError("implementing this method in the subclasses")

#simple query translator
class SimpleQueryTraslator(BaseQueryTranslator):

    def __init__(self, llm: BaseChatModel=ChatOpenAI(temperature=0)):
        super().__init__()
        self.llm = llm
        self.prompt_enhancer: ChatPromptTemplate = ChatPromptTemplate.from_template(QueryPrompts().SIMPLE_TEMPLATE)
    
    def invoke(self, query):
        # response = self.prompt_enhancer | self.llm | StrOutputParser()
        # enhanced_queries = response.invoke({"question":query})
        #return enhanced_queries.split("\n")
        return SingleQuery(query = query, is_modified=False, updated_query=None) 

#Query enhancer
class QueryEnhancerTraslator(BaseQueryTranslator):

    def __init__(self,llm: BaseChatModel=ChatOpenAI(temperature=0)):
        super().__init__()
        self.llm = llm
        self.prompt_enhancer = ChatPromptTemplate.from_template(QueryPrompts().ENHANCER_TEMPLATE)
    
    def invoke(self, query):
        response = self.prompt_enhancer | self.llm | StrOutputParser()
        enhanced_queries = response.invoke({"question":query})
        return enhanced_queries.split("\n")

#Query decomposer to subtasks or subquiers
class QueryDecomposition(BaseQueryTranslator):
    def __init__(self,llm: BaseChatModel=ChatOpenAI(temperature=0)):
        super().__init__()
        self.llm = llm
        self.prompt_decomposition= ChatPromptTemplate.from_template(QueryPrompts().DECOMPOSITION_TEMPLATE)

    def invoke(self, query) -> UserQuery:
        response = self.prompt_decomposition | self.llm | StrOutputParser()
        sub_questions = response.invoke({"question":query})
        return sub_questions.split("\n")
        
QUERY_TRANSLATOR_MAP = {
    "simple" : SimpleQueryTraslator,
    "enhancer" : QueryEnhancerTraslator,
    "decompose" : QueryDecomposition
}

class QueryTranslator:
    def __init__(self, ):
        self.cls = QUERY_TRANSLATOR_MAP[Config().QUERY_TRANSLATOR]() 
    
    def invoke(self, query: str) -> UserQuery:
        return self.cls.invoke(query=query)
        
