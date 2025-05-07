import yfinance as yf
import pandas as pd
import requests
import streamlit as st


EURI_API_KEY = st.secrets["EURI_API_KEY"]
GEMINI_FLASH_MODEL = "gemini-2.0-flash-001"
ALPHA_VANTAGE_KEY = st.secrets["ALPHA_VANTAGE_KEY"]

def get_stock_data(ticker: str, period="6mo"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
    except Exception:
        hist, info = get_from_alpha_vantage(ticker)
    return hist, info

def get_from_alpha_vantage(ticker: str):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_KEY,
        "outputsize": "compact"
    }
    r = requests.get(url, params=params).json()
    ts = r.get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(ts, orient="index").sort_index()
    df = df.rename(columns={"5. adjusted close": "Close"})
    df["Close"] = df["Close"].astype(float)
    df.index = pd.to_datetime(df.index)
    return df.tail(120), {"shortName": ticker, "sector": "N/A", "marketCap": "N/A", "longBusinessSummary": "N/A"}

def calculate_indicators(df):
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    df['Volume'] = df.get('Volume', pd.Series(0))

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def get_real_time_sentiment(ticker: str):
    prompt = f"Search the latest 3 news about {ticker}. Summarize sentiment and cite headlines."
    payload = {
        "model": GEMINI_FLASH_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 700,
        "temperature": 0.5
    }
    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.euron.one/api/v1/euri/alpha/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def analyze_stock(ticker: str, period="6mo"):
    hist, info = get_stock_data(ticker, period)
    hist = calculate_indicators(hist)
    sentiment = get_real_time_sentiment(ticker)
    return hist, info, sentiment
