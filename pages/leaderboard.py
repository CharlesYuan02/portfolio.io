import os
import pandas as pd
import streamlit as st 
import supabase
import threading
import warnings
import yfinance as yf 
from src.utils import get_users


def get_portfolio_value(email):
    '''
    Given a user's email, retrieves the total principal invested in their portfolio.
    Then, calculate the current value of the portfolio.
    
    Args:
        email (str): The email of the user
    
    Returns:
        portfolio_names (list): A list of the portfolio names
        total_returns (list): A list of the total returns for each portfolio
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    STOCK_DATA_TABLE = os.environ.get("STOCK_DATA_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    response = client.table(STOCK_DATA_TABLE).select("*").eq("owner", email).execute()
    df = pd.DataFrame.from_dict(response.data)

    if df.empty:
        return [], []

    # Only display percentage returns 
    total_returns = []
    portfolio_names = []

    # Loop through all unique portfolios
    for portfolio in df["portfolio"].unique():
        # Filter the dataframe by the current portfolio and create a copy
        portfolio_df = df[df["portfolio"] == portfolio].copy()

        # Calculate the total principal invested
        portfolio_df["total_value"] = portfolio_df["unit_price"] * portfolio_df["amount"]
        total_principal = portfolio_df["total_value"].sum()

        # Calculate the current value of the portfolio (as of prev day's close)
        current_value = 0
        for _, row in portfolio_df.iterrows():
            stock = yf.Ticker(row["stock"])
            current_value += stock.history(period="1d")["Close"].values[0] * row["amount"]
        
        # Calculate the total return as a percentage
        total_return = ((current_value - total_principal) / total_principal) * 100
        total_returns.append(total_return)
        portfolio_names.append(portfolio)
    
    return portfolio_names, total_returns


if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.switch_page("app.py")

    st.title("Leaderboard")

    # Suppress FutureWarnings due to internal yfinance implementation details
    warnings.simplefilter(action='ignore', category=FutureWarning)

    with st.spinner("Loading..."):
        # Retrieve all users from the users table
        users = get_users()

        # Multithread the retrieval of portfolio values for each user
        leaderboard = []
        threads = []
        for user in users:
            thread = threading.Thread(target=get_portfolio_value, args=(user,))
            thread.start()
            threads.append(thread)
            
            portfolio_names, total_returns = get_portfolio_value(user)
            if not portfolio_names or not total_returns:
                continue
            for i in range(len(portfolio_names)):
                total_returns[i] = "{:.2f}%".format(total_returns[i])
                leaderboard.append((user, portfolio_names[i], total_returns[i]))

        for thread in threads:
            thread.join()
        
        # Sort the leaderboard in descending order and display
        leaderboard.sort(key=lambda x: x[2], reverse=True)
        df = pd.DataFrame(leaderboard, columns=["Email", "Portfolio Name", "Total Return"])
        df.index = range(1, len(df) + 1) # Index starting from 1
        st.write("Here are the top portfolios on the platform!")
        st.table(df)

    

    
    
    

