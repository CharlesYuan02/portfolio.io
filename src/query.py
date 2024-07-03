import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore


def vector_search(ticker, query):
    '''
    Performs vector search on Pinecone to retrieve relevant embeddings
    while filtering results based on ticker specified.
    Uses OpenAI's gpt-3.5-turbo to generate a response given the retrieved embeddings.

    Args:
        ticker (str): The stock ticker (e.g. AAPL) specified for filtering.
        query (str): The question inputted by the user.

    Returns:
        retriever_output (str): The chatbot's answer.
    '''
    load_dotenv()
    os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")

    # Define the filter based on the metadata field and value
    vector_search = PineconeVectorStore(
        embedding=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        index_name=os.getenv("VECTOR_SEARCH_INDEX"),
    )

    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )
    
    retriever = vector_search.as_retriever(search_kwargs={"k": 5, "filter": {"ticker": ticker}})
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    
    # Inject ticker into query to filter documents
    retriever_output = qa.invoke({"query": ticker + ": " + query})["result"]
    return retriever_output.replace("$", "\$").lstrip() # Escape dollar signs to prevent LaTeX rendering issues
    
if __name__ == "__main__":
    print(vector_search("AAPL", "How much did Americas net sales decrease in 2023 compared to Europe?"))