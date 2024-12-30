from fastapi import APIRouter, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from dataclasses import dataclass, asdict

from src.translator import QueryTranslator
from src.retriever import QueryRetriever
from src.generator import QueryGenerator 
from src.indexer import ChromaVectorStore
from src.router import QueryRouter
from src.router import RouterDecision
from src.crawler import GitHubCrawler
from src.indexer import DocumentIndexer


import logging
logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@dataclass
class QueryModel():
    query : str
    
@dataclass
class AgentResponse():
    query : str
    user_output: str
    documents  : list[str] 


@app.post("/query/")
async def handle_query(query_model: QueryModel):
    try:
        logger.info("Received query: %s", query_model.query)
        query = query_model.query
        vector_store  = ChromaVectorStore().get_vectorstore()
        user_query    = QueryTranslator().invoke(query=query)
        r_decision    = QueryRouter(vector_store=vector_store).invoke(query=user_query)
        context       = QueryRetriever().invoke(router_decision=r_decision)
        user_output   = QueryGenerator().invoke(context=context)
        agent_obj     = AgentResponse(query=query, user_output=user_output, documents=context.docs,)
        logger.info("Successfully processed the query.")
        return agent_obj
    except Exception as e:
        logger.error("Error processing the query: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

class URLRequest(BaseModel):
    url: str

@app.post("/crawl/")
async def crawl_github(url_request: URLRequest):
    crawler = GitHubCrawler()
    meta_data = crawler.invoke()
    return meta_data

# @app.post("/index/")
# async def index_duplocloud():
#     github_crawler = GitHubCrawler()
#     github_docs = github_crawler.invoke()
#     _ = DocumentIndexer().invoke(docs=github_docs)
#     return "success"

class IndexResponse(BaseModel):
    message: str
    details: str = None

@app.post("/index/", response_model=IndexResponse)
async def index_duplocloud():
    try:
        logger.info("Starting the indexing process.")
        github_crawler = GitHubCrawler()
        github_docs = github_crawler.invoke()
        if not github_docs:
            logger.warning("No documents found to index.")
            return IndexResponse(message="No documents to index", details="The GitHub crawler returned no documents.")
        DocumentIndexer().invoke(docs=github_docs)
        logger.info("Indexing completed successfully.")
        return IndexResponse(message="Success")
    
    except Exception as e:
        logger.error(f"An error occurred during indexing: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during indexing")


#TODO - INCLUDE LIST OF ALL THESE APIS
#githublink collection name github url to index 



