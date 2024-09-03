import os
import supabase


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