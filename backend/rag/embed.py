import edgar
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore


def generate_embeddings(text, ticker, source, chunk_size=1500, chunk_overlap=500):
    '''
    Given the text extracted from a company's 10-K or 10-Q, 
    use OpenAI to generate the vector embeddings and store in Pinecone.
    
    Args:
        text (str): The text extracted from the company's 10-K or 10-Q
        ticker (str): The ticker of the company, for filtering
        source (str): The source of the text (10-K or 10-Q)
        chunk_size (int): The size of the chunks to split the text into
        chunk_overlap (int): The amount of overlap between chunks
    
    Returns:
        embeddings (list): A list of the embeddings generated
    '''

    # Connect to Pinecone
    load_dotenv()
    os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")

    # Split the text into smaller chunks and embed
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(text)

    metadata = []
    for text in texts:
        metadata.append({"ticker": ticker, "source": source, "text": text})

    PineconeVectorStore.from_texts(
        texts,
        embedding=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
        metadatas=metadata,
        index_name=os.getenv("VECTOR_SEARCH_INDEX"),
    )


if __name__ == "__main__":
    ticker = "AAPL"
    source = "10-K"
    NAME = os.environ.get("NAME")
    EMAIL = os.environ.get("EMAIL")
    edgar.set_identity(NAME + " " + EMAIL)
    filings = edgar.Company(ticker).get_filings(form=source).latest(1)
    generate_embeddings(filings.text(), ticker, source)