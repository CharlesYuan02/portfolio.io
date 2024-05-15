import os
import streamlit as st 
import supabase
import yfinance as yf 
from datetime import timedelta
from dotenv import load_dotenv
from src.utils import get_portfolios


def insert_into_supabase(ticker, amount, date, price, total_value, portfolio):
    '''
    Inserts a new position into the user's Supabase table.

    Args:
        ticker (str): The stock ticker (e.g. VOO)
        amount (float): The amount of shares bought (can be fractional)
        date (datetime.date): The datetime.date object corresponding to the purchase date of the shares
        price (float): The price of the shares when bought
        total_value (float): The total value of the new position (price * amount)
        portfolio (str): The name of the portfolio to add the new position to
    
    Returns:
        data (dict): The data of the new position
        count (int): The number of positions added
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    STOCK_DATA_TABLE = os.environ.get("STOCK_DATA_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    data, count = client.table(STOCK_DATA_TABLE).insert(
        {
            "stock": ticker,
            "amount": amount,
            "unit_price": price,
            "total_price": total_value,
            "date_purchased": date.strftime("%Y-%m-%d"),
            "owner": st.session_state["email"],
            "portfolio": portfolio
        }
    ).execute()
    return data, count


def create_new_portfolio(portfolio, is_public):
    '''
    Adds the new portfolio to the portfolios table in Supabase.

    Args:
        portfolio (str): The name of the new portfolio
        is_public (bool): Whether the new portfolio is to be made public or not

    Returns:
        data (dict): The data of the new position
        count (int): The number of positions added
    '''
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    PORTFOLIOS_TABLE = os.environ.get("PORTFOLIOS_TABLE")
    client = supabase.create_client(SUPABASE_URL, SUPABASE_API_KEY)
    data, count = client.table(PORTFOLIOS_TABLE).insert(
        {
            "email": st.session_state["email"],
            "portfolio": portfolio,
            "is_public": is_public
        }
    ).execute()
    return data, count


def add_position(ticker, amount, price, date, portfolio, is_public, is_new_portfolio):
    '''
    Displays the UI for entering a new position. 
    Calls insert_into_supabase to actually register the new position.

    Args:
        ticker (str): The stock ticker (e.g. VOO)
        amount (float): The amount of shares bought (can be fractional)
        date (datetime.date): The datetime.date object corresponding to the purchase date of the shares
        price (float): The price of the shares when bought
        portfolio (str): The name of the portfolio to add the new position to
        is_public (bool): Whether the portfolio is to be made public or not
        is_new_portfolio (bool): Whether the portfolio is new or not
    
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
            st.write(f"Add To: {portfolio}")

            if st.button("Add Position"):
                data, count = insert_into_supabase(ticker, amount, date, price, total_value, portfolio)
                if is_new_portfolio:
                    data_new_portfolio, count_new_portfolio = create_new_portfolio(portfolio, is_public)
                    if data_new_portfolio and count_new_portfolio:
                        st.write("Successfully added new portfolio!")
                    else:
                        st.write("Error adding new portfolio!")
                if data and count:
                    st.write("Successfully added new entry!")
                else:
                    st.write("Error adding new entry!")
    else:
        st.write("No data available for the specified date")


if __name__ == "__main__":
    # Upon refresh of cache/session state, go back to login page
    if "logged_in" not in st.session_state:
        st.switch_page("app.py")

    ticker = st.text_input("Stock Ticker:")
    amount = st.number_input("Amount:", min_value=0)
    fractional = st.number_input("Fractional Amount:", min_value=0.000, step=1e-3, format="%.3f")
    amount += fractional
    price = st.number_input("Purchase Price:", min_value=0.00)
    date = st.date_input("Date Purchased:", format="YYYY-MM-DD")

    # Allow users to have multiple portfolios
    portfolios, are_public = get_portfolios(st.session_state["email"])
    option = st.selectbox(
        "Add To:",
        portfolios + ["Create New"]
    )
    portfolio = option if option != "Create New" else None
    is_public = are_public.get(option, False) # Default to False if portfolio doesn't exist
    if option == "Create New":
        portfolio = st.text_input("New Portfolio Name:")

        # Give user option to make portfolio public
        if option: 
            is_public = st.checkbox("Make Portfolio Public")

    if ticker and amount and price and date:
        load_dotenv()
        is_new_portfolio = (option == "Create New" and portfolio not in portfolios)
        add_position(ticker, amount, price, date, portfolio, is_public, is_new_portfolio)
    
    