from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from config import *
from retriever import VectorDBQueryRetriver
from retriever import Context, ToolQueryRetriever, VectorDBQueryRetriver

# Define the Prompt Template for vector db
VECTORDB_PROMPT_TEMPLATE = """You are an AI assistant tasked with answering questions based on the provided context. Use the following pieces of context to answer the question at the end. If you don't know the answer or if the context doesn't contain relevant information, respond with 'NOT_FOUND' to trigger a web search.
Context:{context}
Question: {question}
Answer:"""

# Define the Prompt Template for tooling
TOOL_PROMPT_TEMPLATE = """You are an helpful AI assistant tasked with answering question based on the provided tool_out .dont change any numeric values. Use the following pieces of context to answer the question at the end. If you don't know the answer or if the context doesn't contain relevant information, respond with 'NOT_FOUND' to trigger a web search.
Context:{tool_out}
Question: {question}
Answer:"""


PROMPT = PromptTemplate(template=VECTORDB_PROMPT_TEMPLATE, input_variables=["context", "question"])
TOOL_PROMPT = PromptTemplate(template=TOOL_PROMPT_TEMPLATE, input_variables=["context", "question"])


# class ToolQueryGenerator:
#     def invoke(self, context : Context) -> str:
#         return context.tool_out 


class ToolQueryGenerator:
    def __init__(self):
        self.TOOL_PROMPT_TEMPLATE = """Enhance the answer You are an helpful AI assistant tasked with answering question based on the provided context .dont change any numeric values. 
                                Context:{tool_out}
                                Question: {question}
                                Answer:"""
        self.TOOL_PROMPT = PromptTemplate(template=TOOL_PROMPT_TEMPLATE, input_variables=["context", "question"])


    def invoke(self, context : Context) -> str:
        tool_out = context.tool_out
        question = context.query
        prompt = ChatPromptTemplate.from_template(self.TOOL_PROMPT_TEMPLATE)
        model = ChatOpenAI()
        prompt_obj = prompt.invoke({"tool_out" : tool_out, "question" : question})
        output = model.invoke(prompt_obj)
        return output

class VectorDBQueryGenerator:
    def __init__(self):
        self.RAG_PROMPT_TEMPLATE = """You are an AI assistant tasked with answering questions based on the provided context. Use the following pieces of context to answer the question at the end. If you don't know the answer or if the context doesn't contain relevant information, respond with 'NOT_FOUND' to trigger a web search.
            Context:{context}
            Question: {question}
            Answer:"""
        self.PROMPT = PromptTemplate(template=self.RAG_PROMPT_TEMPLATE, input_variables=["context", "question"])

        
    def invoke(self, context : Context) -> str:
        docs = context.docs 
        question = context.query
        docs_str = "\n\n".join([d.page_content for d in docs])
        prompt = ChatPromptTemplate.from_template(self.RAG_PROMPT_TEMPLATE)
        model = ChatOpenAI()
        prompt_obj = prompt.invoke({"context" : docs_str, "question" : question})
        output = model.invoke(prompt_obj)
        return output


class QueryGenerator:
    def invoke(self,context : Context) -> str :
        if context.is_tool:
            output : Context = ToolQueryGenerator().invoke(context=context)
        elif context.is_vectordb:
            output : Context = VectorDBQueryGenerator().invoke(context=context)
        return output

 
