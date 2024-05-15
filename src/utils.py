import os
import supabase


def get_users():
    '''
    Retrieves all the users from the users table in Supabase.

    Returns:
        users (list): A list of all the users
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
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
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    PORTFOLIOS_TABLE = os.environ.get("PORTFOLIOS_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    response = client.table(PORTFOLIOS_TABLE).select("portfolio", "is_public").eq("email", email).execute()
    return [row["portfolio"] for row in response.data], {row["portfolio"]: row["is_public"] for row in response.data}