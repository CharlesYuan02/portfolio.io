import os
import plotly.express as px
import streamlit as st
import supabase 
import yfinance as yf 
from dotenv import load_dotenv
from st_pages import Page, show_pages


def register(email, password):
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
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
        load_dotenv()
        successful_registration = register(email, password)
        if successful_registration:
            st.switch_page("pages/home.py")