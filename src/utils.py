import os
import supabase
from dotenv import load_dotenv
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


def get_users():
    '''
    Retrieves all the users's emails and usernames from the users table in Supabase.

    Returns:
        emails (list): A list of all the emails (to use as relational key)
        usernames (list): A list of all the usernames
    '''
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    response = client.table(ALL_USERS_TABLE).select("*").execute()
    return [row["email"] for row in response.data], [row["username"] for row in response.data]


def get_portfolios(email):
    '''
    Retrieves all the portfolios for a given user.

    Args:
        email (str): The user's email
    
    Returns:
        portfolios (list): A list of all the user's portfolios
        are_public (dict): A dictionary mapping each portfolio to whether it is public or not
    '''
    load_dotenv()
    PORTFOLIOS_TABLE = os.environ.get("PORTFOLIOS_TABLE")
    client = get_supabase_client()
    response = client.table(PORTFOLIOS_TABLE).select("portfolio", "is_public").eq("email", email).execute()
    return [row["portfolio"] for row in response.data], {row["portfolio"]: row["is_public"] for row in response.data}


def get_tickers():
    '''
    Retrieves all unique stock tickers from the Pinecone index metadata.

    Returns:
        tickers (list): A list of all unique stock tickers
    '''
    load_dotenv()
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