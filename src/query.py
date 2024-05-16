import os
import pymongo
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_mongodb import MongoDBAtlasVectorSearch


def vector_search(ticker, query):
    '''
    Performs vector search on MongoDB Atlas vector store to retrieve relevant embeddings
    while filtering results based on ticker specified.
    Uses OpenAI's gpt-3.5-turbo to generate a response given the retrieved embeddings.

    Args:
        ticker (str): The stock ticker (e.g. AAPL) specified for filtering.
        query (str): The question inputted by the user.

    Returns:
        retriever_output (str): The chatbot's answer.
    '''
    CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
    pymongo_client = pymongo.MongoClient(CLUSTER_NAME)
    collection = pymongo_client[DB_NAME][COLLECTION_NAME]

    # Define the filter based on the metadata field and value
    vector_search = MongoDBAtlasVectorSearch(
        embedding=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
        collection=collection,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )
    
    retriever = vector_search.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    
    # Inject ticker into query to filter documents
    retriever_output = qa.invoke({"query": ticker + ": " + query})["result"]
    return retriever_output
    
if __name__ == "__main__":
    load_dotenv()
    print(vector_search("AAPL", "How much did Americas net sales decrease in 2023 compared to Europe?"))