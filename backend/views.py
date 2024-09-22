import json
import os
import yfinance as yf
from collections import defaultdict
from datetime import datetime, timedelta
from django.core.cache import cache
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from .utils import get_supabase_client, retrieve_tickers
from .rag.chatbot import vector_search


def cache_all_portfolios(client, table_name, email, portfolios):
    '''
    Helper function for caching all the user's portfolios in the database.

    Args:
        client (supabase.Client): The Supabase client
        table_name (str): The name of the table to retrieve the data from
        email (str): The user's email
        portfolios (list): A list of the user's portfolios
    '''
    for portfolio in portfolios:
        response = client.table(table_name).select("*").eq("owner", email).eq("portfolio", portfolio).execute()

        info = {
            "performance": [], # [[date, total_value], ...]
            "positions": {}, # {stock: {total_value, total_shares}}
            "history": [] # [{stock, amount, unit_price, total_price, date_purchased}]
        }

        # Sum up the total value of each stock in the portfolio
        combined_price_history = defaultdict(float)
        for row in response.data:
            stock, amount, total_price = row["stock"], row["amount"], row["total_price"]
            stock_data = yf.download(stock, start=row["date_purchased"], progress=False)

            if stock in info["positions"]:
                info["positions"][stock]["total_value"] += total_price
                info["positions"][stock]["total_shares"] += amount
            else:
                info["positions"][stock] = {
                    "total_value": total_price,
                    "total_shares": amount
                }

            # Populate history of transactions
            info["history"].append({
                "stock": stock,
                "amount": amount,
                "unit_price": row["unit_price"],
                "total_price": total_price,
                "date_purchased": row["date_purchased"]
            })
            info["history"] = sorted(info["history"], key=lambda x: x["date_purchased"])

            # Update combined_price_history
            for date, row in stock_data.iterrows():
                date = date.strftime("%Y-%m-%d")
                combined_price_history[date] += row['Close'] * amount

        combined_price_history = sorted([[date, value] for date, value in combined_price_history.items()])
        info["performance"] = combined_price_history

        # Store in cache with email, portfolio as key
        portfolio_name = portfolio.replace(" ", "_").lower()
        cache_key = f"{email}_{portfolio_name}"
        cache.set(cache_key, info) # Timeout is set in settings, 3600s


@api_view(["POST"])
def get_all_portfolios(request):
    '''
    Endpoint for retrieving all the portfolios for a given user.

    Args:
        email (str): The user's email
    
    Returns:
        portfolios (list): A list of all the user's portfolios
        [Excluded] are_public (dict): A dictionary mapping each portfolio to whether it is public or not
    '''
    load_dotenv()
    PORTFOLIOS_TABLE = os.environ.get("PORTFOLIOS_TABLE")
    STOCK_DATA_TABLE = os.environ.get("STOCK_DATA_TABLE")
    client = get_supabase_client()

    # Extract email from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]

    # Fetch all the user's portfolios
    response = client.table(PORTFOLIOS_TABLE).select("portfolio", "is_public").eq("email", email).execute()
    portfolios = [row["portfolio"] for row in response.data]

    # Store in cache
    cache_all_portfolios(client, STOCK_DATA_TABLE, email, portfolios)

    return JsonResponse(portfolios, safe=False) # , {row["portfolio"]: row["is_public"] for row in response.data}


@api_view(["POST"])
def get_portfolio_performance(request):
    '''
    Endpoint for retrieving the performance of a given portfolio.

    Args:
        email (str): The user's email
        portfolio (str): The name of the portfolio

    Returns:
        performance (list): A list of the portfolio's performance data
        [[date, total_value], ...]
    '''
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]
    portfolio_name = portfolio.replace(" ", "_").lower()

    # Fetch the portfolio performance data from the cache
    cache_key = f"{email}_{portfolio_name}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["performance"], safe=False)


@api_view(["POST"])
def get_portfolio_holdings(request):
    '''
    Endpoint for retrieving the holdings of a given portfolio.

    Args:
        email (str): The user's email
        portfolio (str): The name of the portfolio

    Returns:
        positions (dict): A dictionary of the portfolio's positions
        {stock: {total_value, total_shares}}    
    '''
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]
    portfolio_name = portfolio.replace(" ", "_").lower()

    # Fetch the portfolio holdings data from the cache
    cache_key = f"{email}_{portfolio_name}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["positions"])


@api_view(["POST"])
def get_portfolio_history(request):
    '''
    Endpoint for retrieving the history of a given portfolio.

    Args:
        email (str): The user's email
        portfolio (str): The name of the portfolio

    Returns:
        history (list): A list of the portfolio's history data
        [{stock, amount, unit_price, date_purchased, action}]
    '''
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]
    portfolio_name = portfolio.replace(" ", "_").lower()

    # Fetch the portfolio history data from the cache
    cache_key = f"{email}_{portfolio_name}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["history"], safe=False)


@api_view(["POST"])
def get_daily_price_range(request):
    '''
    Endpoint for retrieving the daily price range of a given stock.
    
    Args:
        ticker (str): The stock ticker (e.g. AAPL)
        date (str): The date for which the price range is requested (YYYY-MM-DD)
    
    Returns:
        price_range (tuple): A tuple containing the stock's daily price range (low, high)
    '''
    # Extract ticker from POST request body
    data = json.loads(request.body.decode("utf-8"))
    ticker = data["ticker"]
    date_str = data["date"].split("T")[0] # Remove timezone info
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # Fetch the daily price range of the stock
    next_day = date + timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    stock_data = yf.download(ticker, start=date_str, end=next_day_str, progress=False)
    low, high = stock_data["Low"].values[0], stock_data["High"].values[0]
    return JsonResponse((low, high), safe=False)


@api_view(["POST"])
def get_premium(request):
    '''
    Endpoint for retrieving the premium status of a given user.

    Args:
        email (str): The user's email

    Returns:
        is_premium (bool): A boolean indicating whether the user is a premium user
    '''
    # Extract email from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]

    # Check if the user is a premium user by retrieving from Supabase
    load_dotenv()
    ALL_USERS_TABLE = os.environ.get("ALL_USERS_TABLE")
    client = get_supabase_client()
    response = client.table(ALL_USERS_TABLE).select("is_premium").eq("email", email).execute()
    is_premium = response.data[0]["is_premium"]
    return JsonResponse(is_premium, safe=False)


@api_view(["GET"])
def get_tickers(request):
    '''
    Endpoint for retrieving all the unique stock tickers from the Pinecone index metadata.

    Returns:
        tickers (list): A list of all unique stock tickers
    '''
    load_dotenv()
    tickers = retrieve_tickers()
    return JsonResponse(tickers, safe=False)


@api_view(["POST"])
def get_chatbot_response(request):
    '''
    Endpoint for retrieving the chatbot response given a user query.

    Args:
        ticker (str): The stock ticker (e.g. AAPL) specified for filtering.
        query (str): The question inputted by the user.
    
    Returns:
        response (str): The chatbot's answer.
    '''
    # Extract ticker and query from POST request body
    data = json.loads(request.body.decode("utf-8"))
    ticker = data["ticker"]
    query = data["query"]

    # Perform vector search and generate chatbot response
    response = vector_search(ticker, query)
    return JsonResponse(response, safe=False)