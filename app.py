import os
import plotly.express as px
import streamlit as st
import yfinance as yf 
from dotenv import load_dotenv
from st_pages import Page, show_pages
from src.utils import get_supabase_client


def login(email, password):
    '''
    Takes the user inputted email and password, then performs the following:
        1. If user email is not within database, prompt redirect to the sign up page.
        2. If user email is within database but password incorrect, prompt a retry.
        3. If user email and password are correct, indicate successful login.
    
    Args:
        email (str): User's email
        password (str): User's password (can be alphanumeric)

    Returns:
        correct_email (bool): Indicates whether email is within database or not
        correct_password (bool): Indicates whether user entered correct password or not
    '''
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    response = client.table(ALL_USERS_TABLE).select("*").eq("email", email).execute()
    if not response.data:
        return False, False # New user
    if response.data and response.data[0]["password"] == password:
        st.session_state["email"] = email
        return True, True # Successful login
    return True, False # User entered wrong password


def view_stock_price():
    '''
    Basic homepage. Retrieves a stock's price history and displays it on a line graph.
    '''
    ticker = st.text_input("Stock Ticker:")
    timeframe_options = ["ytd", "5d", "1mo", "3mo", "6mo", "1y", "3y", "5y", "10y", "max"]
    timeframe = st.selectbox("Timeframe", timeframe_options)
    if ticker:
        data = yf.Ticker(ticker).history(period=timeframe)
        open = data["Open"]
        close = data["Close"]
        fig = px.line(x=data.index, y=[open, close])
        fig.update_layout(
            title=f"{ticker} Historical Prices",
            xaxis_title="History",
            yaxis_title=f"{ticker} Price (USD)",
            legend_title=""
        )
        fig.data[0].name = "Open Price"
        fig.data[1].name = "Close Price"

        st.plotly_chart(fig)


if __name__ == "__main__":
    # Don't reset to False on every page load
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Only display login logic when user is not logged in 
    if not st.session_state["logged_in"]:
        st.title("Login")

        # home.py needs to be shown to be switched to, but shouldn't show up in sidebar
        show_pages(
            [
                Page("app.py", "Login"),
                Page("pages/signup.py", "Sign Up"),
                Page("pages/home.py", "")
            ]
        )
        email = st.text_input("Email:")
        password = st.text_input("Password:")
        login_press = st.button("Login")
        
        if email and password and login_press:
            correct_email, correct_password = login(email, password)
            if not correct_email:
                st.error("Email entered incorrectly or user is not registered.")

            if correct_email and correct_password:
                st.text("Success!")
                st.session_state["logged_in"] = True
                st.switch_page("pages/home.py")
                    
            elif correct_email and not correct_password:
                st.error("Incorrect password, please try again.")