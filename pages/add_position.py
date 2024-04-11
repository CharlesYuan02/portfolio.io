import os
import streamlit as st 
import supabase
import yfinance as yf 
from datetime import timedelta
from dotenv import load_dotenv


def insert_into_supabase(ticker, amount, date, price, total_value):
    '''
    Inserts a new position into the user's Supabase table.

    Args:
        ticker (str): The stock ticker (e.g. VOO)
        amount (float): The amount of shares bought (can be fractional)
        date (datetime.date): The datetime.date object corresponding to the purchase date of the shares
        price (float): The price of the shares when bought
        total_value (float): The total value of the new position (price * amount)
    
    Returns:
        None
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    TABLE_NAME = os.environ.get("TABLE_NAME") # TODO: Change this for different users
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    data, count = client.table(TABLE_NAME).insert(
        {
            "stock": ticker,
            "amount": amount,
            "unit_price": price,
            "total_price": total_value,
            "date_purchased": date.strftime("%Y-%m-%d")
        }
    ).execute()
    return data, count


def add_position(ticker, amount, price, date):
    '''
    Displays the UI for entering a new position. 
    Calls insert_into_supabase to actually register the new position.

    Args:
        ticker (str): The stock ticker (e.g. VOO)
        amount (float): The amount of shares bought (can be fractional)
        date (datetime.date): The datetime.date object corresponding to the purchase date of the shares
        price (float): The price of the shares when bought
    
    Returns:
        None
    '''
    stock = yf.Ticker(ticker)
        
    # Get datestr of next day 
    next_day = date + timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    stock_data = stock.history(start=date, end=next_day_str)

    if not stock_data.empty:
        high_price = stock_data["High"].values[0]
        low_price = stock_data["Low"].values[0]
        if price > high_price or price < low_price:
            st.error(f"Price entered not within day range: {low_price:.2f} - {high_price:.2f}")
        else:
            total_value = amount * price
            st.write(f"Stock: {ticker}")
            st.write(f"Amount: {amount}")
            st.write(f"Date: {date}")
            st.write(f"Price: ${price:.2f}")
            st.write(f"Total Value: ${total_value:.2f}")

            if st.button("Add Position"):
                data, count = insert_into_supabase(ticker, amount, date, price, total_value)
                if data and count:
                    st.write("Success!")
                else:
                    st.write("Error!")
    else:
        st.write("No data available for the specified date")


if __name__ == "__main__":
    ticker = st.text_input("Stock Ticker:")
    amount = st.number_input("Amount:", min_value=0)
    fractional = st.number_input("Fractional Amount:", min_value=0.000, step=1e-3, format="%.3f")
    amount += fractional
    price = st.number_input("Purchase Price:", min_value=0.00)
    date = st.date_input("Date Purchased:", format="YYYY-MM-DD")

    if ticker and amount and price and date:
        load_dotenv()
        add_position(ticker, amount, price, date)