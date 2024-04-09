import plotly.express as px
import streamlit as st 
import yfinance as yf 


def view_stock_price():
    '''
    Basic homepage. Retrieves a stock's price history and displays it on a line graph.
    
    Args:
        None

    Returns:
        None
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
    view_stock_price()
