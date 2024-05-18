import os
import streamlit as st
from dotenv import load_dotenv
from st_pages import Page, show_pages
from src.utils import get_supabase_client


def register(email, password):
    '''
    Basic homepage. Retrieves a stock's price history and displays it on a line graph.
    
    Args:
        email (str): User's email
        password (str): User's password (can be alphanumeric)

    Returns:
        successful_registration (bool): Whether the user successfully registered (fails if user already exists)
    '''
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    response = client.table(ALL_USERS_TABLE).select("*").eq("email", email).execute()
    if not response.data:
        client.table(ALL_USERS_TABLE).insert(
            {
                "email": email,
                "password": password,
            }
        ).execute()
        st.session_state["email"] = email
        return True
    
    return False # User already exists


if __name__ == "__main__":
    st.title("Sign Up")
    show_pages(
        [
            Page("app.py", "Login"),
            Page("pages/signup.py", "Sign Up"),
            Page("pages/home.py", "")
        ]
    )

    email = st.text_input("Email:")
    password = st.text_input("Password:")
    login_press = st.button("Register")
    if email and password and login_press:
        successful_registration = register(email, password)
        if successful_registration:
            st.switch_page("pages/home.py")