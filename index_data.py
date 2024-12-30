from src.indexer import DocumentIndexer
from src.crawler import GitHubCrawler

def index_data():
    github_crawler = GitHubCrawler()
    github_docs = github_crawler.invoke()
    _ = DocumentIndexer().invoke(docs=github_docs)
    