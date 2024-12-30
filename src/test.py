from translator import QueryTranslator
from router import ChromaDBChecker, TavilyDBChecker, InbuiltFunctionChecker, LogicalRouter
from indexing import ChromaIndex
from config import urls
from retriever import DBRetriever
from generator import InbuiltGenerator
from config import urls


if __name__ == "__main__":


    #1. translate
    print("Step 1: Translating the user query ------------------------------------------------>")
    question = "what is duplocloud?"
    simple_translator = QueryTranslator()
    simple_query_result = simple_translator.invoke(query=question)
    print(simple_query_result)
    
    #2. Route
    #TBD
    
    #.3.Index 
    print("Step 3: Indexing the VectorDB --------------------------------------------------->")
    downloader = ChromaIndex(chroma_storage=urls.CHROMA_STORAGE)
    vectordb = downloader.download_to_chroma(urls.GITURL)

    #4. Retrive
    print("Step 4: Retriving the context --------------------------------------------------->")
    retriever = DBRetriever()
    retriever_instance = retriever.retrieve(vectordb=vectordb)


    #5. Generate
    print("Step 5: Generating the the results --------------------------------------------------->")
    generator = InbuiltGenerator(retriever=retriever_instance)
    response = generator.generate(question)
    print(f"Question: {question}\nResponse: {response}")


























    # question = "what is duplocloud?"

    # # Initialize SimpleQueryTranslator with the required LLM
    # simple_translator = QueryTranslator()
    # simple_query_result = simple_translator.invoke(query=question)

    # print("\nSimple Query Translator ======================")
    # print("\n".join(simple_query_result))


    # # Initialize the downloader and process the URL
    # downloader = Chromaindex(chroma_storage=urls.CHROMA_STORAGE)
    # vectordb = downloader.download_to_chroma(urls.GITURL)  


    # # chroma_checker = ChromaDBChecker(vectordb)
    # # chroma_bool    =  chroma_checker.check_query(query=question)
    # # print(chroma_checker)


    # # tavily_checker = TavilyDBChecker()

    # # tavily_bool =   tavily_checker.check_query(query=question)
    # # inbuilt_functions_checker = InbuiltFunctionChecker()

    # # router = LogicalRouter()

    #     # Configure the retriever
    # retriever = ChromaDBRetriever()
    # retriever_instance = retriever.retrieve(vectordb=vectordb)

    # generator = InbuiltGenerator(retriever=retriever_instance)

    # question = "what is duplocloud?"

    # response = generator.generate(simple_query_result)
    # print(f"Question: {question}\nResponse: {response}")

    # downloader = ChromaIndex(chroma_storage=urls.CHROMA_STORAGE)
    # vectordb = downloader.download_to_chroma(urls.GITURL)

    # # Configure the retriever
    # retriever = ChromaDBRetriever()
    # retriever_instance = retriever.retrieve(vectordb=vectordb)

    # # Initialize the generator
    # generator = InbuiltGenerator(retriever=retriever_instance)

    # # Query the generator
    # question = "Tell about duplocloud?"
    # response = generator.generate(question)
    # print(f"Question: {question}\nResponse: {response}")
