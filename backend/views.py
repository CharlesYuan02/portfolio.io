import json
import os
import pandas as pd
import yfinance as yf
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .utils import get_supabase_client


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
        for row in response.data:
            stock, amount, total_price = row["stock"], row["amount"], row["total_price"]

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
                "stock": row["stock"],
                "amount": row["amount"],
                "unit_price": row["unit_price"],
                "total_price": row["total_price"],
                "date_purchased": row["date_purchased"]
            })

        # Calculate performance of portfolio over time
        df = pd.DataFrame.from_dict(response.data)
        grouped = df.groupby("stock")
        combined_price_history = pd.DataFrame()

        # Iterate over groups and calculate price history in bulk
        for stock, group in grouped:
            stock_data = yf.download(stock, start=group["date_purchased"].min(), progress=False)
            for _, row in group.iterrows():
                # Filter stock data starting from date_purchased
                relevant_data = stock_data.loc[row["date_purchased"]:]
                combined_price_history[row["stock"]] = relevant_data["Close"] * row["amount"]

        # Sum across rows to get total portfolio value
        combined_price_history.index = combined_price_history.index.strftime("%Y-%m-%d")
        combined_price_history["total_value"] = combined_price_history.sum(axis=1)
        portfolio_value_over_time = combined_price_history[["total_value"]].reset_index().values.tolist()
        
        # Store in cache
        info["performance"] = portfolio_value_over_time

        # Store in cache with email, portfolio as key
        cache_key = f"{email}_{portfolio}"
        cache.set(cache_key, info) # Timeout is set in settings, 3600s


@require_http_methods(["POST"])
@csrf_exempt
def get_all_portfolios(request):
    '''
    Helper function for retrieving all the portfolios for a given user.

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


@require_http_methods(["POST"])
@csrf_exempt
def get_portfolio_performance(request):
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]

    # Fetch the portfolio performance data from the cache
    cache_key = f"{email}_{portfolio}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["performance"], safe=False)


@require_http_methods(["POST"])
@csrf_exempt
def get_portfolio_holdings(request):
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]

    # Fetch the portfolio holdings data from the cache
    cache_key = f"{email}_{portfolio}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["positions"])


@require_http_methods(["POST"])
@csrf_exempt
def get_portfolio_history(request):
    # Extract email and portfolio from POST request body
    data = json.loads(request.body.decode("utf-8"))
    email = data["email"]
    portfolio = data["portfolio"]

    # Fetch the portfolio history data from the cache
    cache_key = f"{email}_{portfolio}"
    portfolio_data = cache.get(cache_key)
    return JsonResponse(portfolio_data["history"], safe=False)