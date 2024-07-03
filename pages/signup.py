import os
import streamlit as st
from dotenv import load_dotenv
from st_pages import Page, show_pages
from src.utils import get_supabase_client, get_users


def register(username, email, password):
    '''
    Basic homepage. Retrieves a stock's price history and displays it on a line graph.
    
    Args:
        username (str): User's username
        email (str): User's email
        password (str): User's password (can be alphanumeric)

    Returns:
        None
    '''
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    client.table(ALL_USERS_TABLE).insert(
        {
            "username": username,
            "email": email,
            "password": password,
        }
    ).execute()
    st.session_state["email"] = email


if __name__ == "__main__":
    st.title("Sign Up")
    show_pages(
        [
            Page("app.py", "Login"),
            Page("pages/signup.py", "Sign Up"),
            Page("pages/home.py", "")
        ]
    )

    emails, usernames = get_users()
    username = st.text_input("Username:")
    if username in usernames:
        st.write("Username already taken.")
        
    email = st.text_input("Email:")
    if email in emails:
        st.write("Account already exists. Please login.")
        st.stop()
    
    password = st.text_input("Password:")
    login_press = st.button("Register")
    if username and username not in usernames and email and email not in emails and password and login_press:
        successful_registration = register(username, email, password)
        if successful_registration:
            st.switch_page("pages/home.py")
    elif not username and login_press:
        st.write("Please enter a username.")
    elif not email and login_press:
        st.write("Please enter an email.")
    elif not password and login_press:
        st.write("Please enter a password.")