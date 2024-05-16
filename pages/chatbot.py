import streamlit as st
from src.query import vector_search
from src.utils import get_tickers


if __name__ == '__main__':
    if "logged_in" not in st.session_state:
        st.switch_page("app.py")
    
    st.title("AI Stock Insights")
    
    # Dropdown menu for user to select a stock
    tickers = get_tickers()
    stock = st.selectbox("Stock", tickers)
    user_input = st.text_input("Ask me anything about a stock!")

    # Button
    if st.button("Ask") and stock and user_input:
        with st.spinner("Thinking..."):
            response = vector_search(stock, user_input)
            if response == " I don't know.": # Idk why there's a space before the "I don't know."
                response = "I could not find any information on that in my sources. Please try a different question."
            if response:
                st.write("AI Response:")
                st.write(response)