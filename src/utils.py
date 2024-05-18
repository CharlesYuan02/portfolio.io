import os
import pymongo
import supabase
import logging
from dotenv import load_dotenv

# Suppress the "Waiting for suitable server to become available" error pymongo logs
logging.getLogger('pymongo').setLevel(logging.WARNING)


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


def get_mongo_collection():
    '''
    Creates a MongoDB collection using the environment variables.
    Assumes load_dotenv() is always called before this function.

    Returns:
        collection (pymongo.collection.Collection): The MongoDB collection
    '''
    CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
    DB_NAME = os.environ.get("DB_NAME")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
    pymongo_client = pymongo.MongoClient(CLUSTER_NAME)
    return pymongo_client[DB_NAME][COLLECTION_NAME]


def get_users():
    '''
    Retrieves all the users from the users table in Supabase.

    Returns:
        users (list): A list of all the users
    '''
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    response = client.table(ALL_USERS_TABLE).select("*").execute()
    return [row["email"] for row in response.data]


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
    Retrieves all unique stock tickers from MongoDB.

    Returns:
        tickers (list): A list of all unique stock tickers
    '''
    load_dotenv()
    collection = get_mongo_collection()

    # Get all unique stock tickers
    tickers = collection.distinct("ticker")
    return tickers