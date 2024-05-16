import edgar
import os
import pymongo
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from tqdm import tqdm


def generate_embeddings(text, ticker, source, chunk_size=1500, chunk_overlap=500):
    '''
    Given the text extracted from a company's 10-K or 10-Q, 
    use OpenAI to generate the vector embeddings and store in 
    MongoDB Atlas Vector Store.
    
    Args:
        text (str): The text extracted from the company's 10-K or 10-Q
        ticker (str): The ticker of the company, for filtering
        source (str): The source of the text (10-K or 10-Q)
        chunk_size (int): The size of the chunks to split the text into
        chunk_overlap (int): The amount of overlap between chunks
    
    Returns:
        embeddings (list): A list of the embeddings generated
    '''

    # Connect to MongoDB Atlas
    CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
    DB_NAME = os.environ.get("DB_NAME")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
    ATLAS_VECTOR_SEARCH_INDEX_NAME = os.environ.get("ATLAS_VECTOR_SEARCH_INDEX_NAME")
    pymongo_client = pymongo.MongoClient(CLUSTER_NAME)
    collection = pymongo_client[DB_NAME][COLLECTION_NAME]

    # Split the text into smaller chunks and embed
    text_splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap)
    texts = text_splitter.split_text(text)

    for text in tqdm(texts):
        MongoDBAtlasVectorSearch.from_texts(
            [text], # You have to pass in a list or else it will not work properly
            embedding=OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY")),
            metadatas=[
                {
                    "ticker": ticker,
                    "source": source,
                }
            ],
            collection=collection,
            index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        )


if __name__ == "__main__":
    load_dotenv()
    ticker = "MSFT"
    source = "10-Q"
    NAME = os.environ.get("NAME")
    EMAIL = os.environ.get("EMAIL")
    edgar.set_identity(NAME + " " + EMAIL)
    filings = edgar.Company(ticker).get_filings(form=source).latest(1)
    generate_embeddings(filings.text(), ticker, source)