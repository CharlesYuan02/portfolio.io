import os
import pandas as pd
import plotly.express as px
import streamlit as st 
import supabase
import yfinance as yf 
from dotenv import load_dotenv


def retrieve_from_supabase():
    '''
    Retrieves all positions from a user's Supabase table
    and displays their investment portfolio historical value on a line graph.

    Args:
        None
    
    Returns:
        None
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    STOCK_DATA_TABLE = os.environ.get("STOCK_DATA_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    response = client.table(STOCK_DATA_TABLE).select("*").eq("owner", st.session_state["email"]).execute()
    if not response.data:
        st.error("You have not added any positions yet!")
        return
    df = pd.DataFrame.from_dict(response.data)
    df.sort_values(by="date_purchased", inplace=True)
    display = df.drop(["id", "created_at", "owner"], axis=1)
    display.reset_index(drop=True, inplace=True)
    st.table(display)

    with st.spinner("Loading..."):
        combined_price_history = []
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
    

if __name__ == "__main__":
    # Upon refresh of cache/session state, go back to login page
    if "logged_in" not in st.session_state:
        st.switch_page("app.py")

    if st.button("View Positions"):
        load_dotenv()
        retrieve_from_supabase()