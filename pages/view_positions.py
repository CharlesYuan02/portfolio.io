import os
import pandas as pd
import plotly.express as px
import streamlit as st 
import supabase
import yfinance as yf 
from dotenv import load_dotenv
from src.utils import get_portfolios


def retrieve_from_supabase(portfolio):
    '''
    Retrieves all positions from a user's specified portfolio
    and displays their investment portfolio historical value on a line graph.

    Args:
        portfolio (str): The name of the portfolio to retrieve positions from
    
    Returns:
        None
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    STOCK_DATA_TABLE = os.environ.get("STOCK_DATA_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)

    # Return response using eq with both email and portfolio
    response = client.table(STOCK_DATA_TABLE).select("*").eq("owner", st.session_state["email"]).eq("portfolio", portfolio).execute()
    df = pd.DataFrame.from_dict(response.data)
    df.sort_values(by="date_purchased", inplace=True)
    display = df.drop(["id", "created_at", "owner", "portfolio"], axis=1)
    display.reset_index(drop=True, inplace=True)

    with st.spinner("Loading..."):
        combined_price_history = []
        
        # If all the existing positions are not over a day old, then there is no historical data to display
        # Specifically, one trading day old (must factor in current time)
        current_time = pd.Timestamp.now()
        trading_hours = (current_time.hour >= 9 and current_time.minute > 30) or current_time.hour <= 16
        if (pd.Timestamp.now() - pd.Timestamp(df["date_purchased"].min())).days <= 1 and not trading_hours:
            st.table(display)
            st.write("No historical data to display.")
            st.stop()

        for _, row in df.iterrows():
            stock = yf.download(row["stock"], start=row["date_purchased"])
            closing_price = stock["Close"]
            row_price_history = closing_price * row["amount"]
            combined_price_history.append(row_price_history)
        
        combined_price_history = pd.concat(combined_price_history, axis=1)
        combined_price_history["total_value"] = combined_price_history.sum(axis=1, numeric_only=True)
        fig = px.line(x=combined_price_history.index, y=[combined_price_history["total_value"]])
        fig.update_layout(
                title=f"Portfolio Value",
                xaxis_title="History",
                yaxis_title=f"Total Value (USD)",
                showlegend=False
        )
        st.plotly_chart(fig)
        st.table(display)


if __name__ == "__main__":
    # Upon refresh of cache/session state, go back to login page
    if "logged_in" not in st.session_state:
        st.switch_page("app.py")

    # Create a dropdown menu for all the user's portfolios
    portfolios, _ = get_portfolios(st.session_state["email"])
    if not portfolios:
        st.write("You have not created any portfolios yet! Go to the Add Position page to create one.")
        st.stop()
    else:
        selected_portfolio = st.selectbox("Portfolio:", portfolios)
        if selected_portfolio is not None:
            load_dotenv()
            retrieve_from_supabase(selected_portfolio)