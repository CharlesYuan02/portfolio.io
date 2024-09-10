import os
import supabase
from pinecone import Pinecone


def get_supabase_client():
    '''
    Creates a Supabase client using the environment variables.
    Assumes load_dotenv() is always called before this function.

    Returns:
        client (supabase.Client): The Supabase client
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    return supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)


def retrieve_tickers():
    '''
    Retrieves all unique stock tickers from the Pinecone index metadata.
    Assumes load_dotenv() is always called before this function.

    Returns:
        tickers (list): A list of all unique stock tickers
    '''
    pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pinecone.Index(name=os.getenv("VECTOR_SEARCH_INDEX"))

    # Get the top 10000 results to ensure all tickers are included
    vector_dimension = 1536
    results = index.query(
        vector=[0] * vector_dimension,
        top_k=10000, # Adjust based on dataset size
        include_metadata=True
    )

    # Extract unique tickers from the metadata
    tickers = set()
    for match in results['matches']:
        if 'ticker' in match['metadata']:
            tickers.add(match['metadata']['ticker'])
        
    return list(tickers)