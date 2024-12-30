# AI Agent with RAG and Functional Tooling

This repository is building an **AI Agent** using **Retrieval-Augmented Generation (RAG)** and functional tooling. The agent retrieves relevant information for a user's query by indexing from a **Vector Database** and functional inbuilt tools for generating answers.

## Data Requirement

The data used to index the Vector Database comes from a URL - [DuploCloud Docs](https://github.com/duplocloud/docs/tree/main/getting-started-1/application-focussed-interface) that hosts **Markdown files**. These files are processed and indexed to create embeddings, which are then stored in a vector database [(**Chroma**)]() for efficient similarity search.

## Vector DB Indexing Workflow

The following steps outline how the data is processed and indexed in the Vector Database:

![DB Indexing](assets/Indexing.png)
1. **Extract data from Markdown files**:  Get Docs and preprocess the content from the URL - [DuploCloud Docs](https://github.com/duplocloud/docs/tree/main/getting-started-1/application-focussed-interface).
2. **Generate embeddings**: Convert the docs into chunks and into vector embeddings using pre-trained models from Openai.
3. **Store in Vector DB**: Index the embeddings into a Vector Database for fast retrieval.

## Implementation Workflow

The implementation is divided into multiple components that work together to process queries and retrieve relevant information.

![AI Agent](assets/Workflow.png)

### 1. Query Translator

The **Query Translator** is responsible for transforming user queries into a format suitable for retrieval. There are two primary methods used:

- **Method 1: Simple Query Enhancer**
  - This method translates the user query into a format that matches the retrieval mechanism. It may involve basic enhancements or rephrasing to improve search accuracy.
  
- **Method 2: Query Decomposition**
  - For complex queries, this method splits them into simpler sub-queries that can be handled individually by the retrieval system. This enables the system to process more complex requests efficiently.

### 2. Router

The **Router** directs the query to the appropriate data source based on the type of query. It includes:

- **2.1 Semantic Router**
  - Uses the similarity search logic to route queries to the correct data source (i.e., the Vector Database). It ensures the query is directed to the data source that can provide the most relevant documents based on semantic similarity.

- **2.2 Tooling Router**
  - Routes queries to external tools or systems when the data required is not in the Vector Database. For example, an LLM might be used to fetch contextual information from external sources or databases.

### 3. Retriever

The **Retriever** component is responsible for fetching the most relevant information based on the user query. It works with two types of data sources:

- **3.1 For Vector Database**:
  - The retriever queries the Vector Database (such as **Chroma**) to retrieve the top **k** most relevant documents based on the semantic similarity between the query and indexed documents.

- **3.2 For Tooling**:
  - When the query requires external information (such as real-time data or specialized context), the retriever uses external **tools** (e.g., LLMs, APIs) to fetch the necessary context.

### 4. Generator

The **Generator** component produces the final response based on the user query and the retrieved context. It combines the user’s query with the retrieved data (either from the Vector DB or external tools) and generates an answer.

- The **LLM** (Large Language Model) is used to generate a comprehensive response, taking into account the user’s input and any context retrieved from the Vector Database or external tooling.

## Setup

1. Clone the github repo 
```bash
git clone https://github.com/chandana7d/ai-agent.git
``` 

2. Create .env with the your api keys 
```bash
OPENAI_API_KEY=YOUR_OPENAI_KEY #fjasofindf
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=YOUR_LANGCHAIN_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
COMPOSIO_API_KEY=YOUR_COMPOSIO_API_KEY
BRAVESEARCH_API_KEY = BRAVESEARCH_API_KEY
``` 


### Steps 
1. Build Docker - this also index vetor db 
```bash
docker build -t ai-agent .
``` 

2. Run Docker 
```bash
docker run -p 8000:8000 ai-agent
```
4. Index db - run 

```bash

http://127.0.0.1:8000/index_duplocloud/

{
	"message": "Success",
	"details": null
}
```

3. Run tests for various usecases
```
python src/testing.py 
```
## Author

Contributor details and contact info

Chandana Dayapule  
(https://www.linkedin.com/in/chandanad/)