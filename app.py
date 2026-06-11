import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(layout="wide")
st.title("💹 Interactive Stock Portfolio Dashboard")

# 1. Sidebar Input
st.sidebar.header("User Settings")
ticker_input = st.sidebar.text_input(
    "Enter Tickers (comma separated)", "TSLA,AAPL,MSFT")
# Process the input immediately
tickers = [t.strip().upper() for t in ticker_input.split(",")]

# 2. Main Logic
if st.sidebar.button("Analyze Portfolio"):
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo")

            # --- INDICATORS ---
            hist['RSI'] = ta.rsi(hist['Close'], length=14)
            hist['EMA_50'] = ta.ema(hist['Close'], length=50)
            hist['EMA_200'] = ta.ema(hist['Close'], length=200)
            macd = ta.macd(hist['Close'], fast=12, slow=26, signal=9)
            hist = pd.concat([hist, macd], axis=1)

            # --- DISPLAY ---
            st.subheader(f"Analysis: {ticker}")
            current_price = hist['Close'].iloc[-1]

            col1, col2, col3 = st.columns(3)
            col1.metric("Price", f"${current_price:.2f}")
            col2.metric("RSI", f"{hist['RSI'].iloc[-1]:.2f}")
            col3.metric("MACD", f"{hist['MACD_12_26_9'].iloc[-1]:.2f}")

            st.line_chart(hist[['Close', 'EMA_50', 'EMA_200']])

            # --- NEWS ---
            st.write(f"**Latest News for {ticker}:**")
            try:
                news = stock.news
                for item in news[:3]:
                    st.write(f"- [{item['title']}]({item['link']})")
            except:
                st.write("News currently unavailable.")

            st.divider()

        except Exception as e:
            st.error(f"Could not fetch data for {ticker}: {e}")
else:
    st.info("Enter tickers in the sidebar and click 'Analyze Portfolio'!")
