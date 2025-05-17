import os
import pandas as pd
from config import RAW_STOCK_DIR

def load_ticker_list(csv_path: str) -> list:
    df = pd.read_csv(csv_path)
    return df["Symbol"].tolist()

def load_trading_days(csv_path: str) -> pd.DatetimeIndex:
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    return pd.DatetimeIndex(df["Date"])

def load_price_series(ticker: str) -> pd.Series:
    file_path = os.path.join(RAW_STOCK_DIR, f"{ticker}.csv")
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
        return df["Adj Close"].rename(ticker)
    except Exception as e:
        print(f"[ERROR] {ticker}: {e}")
        return None

def adj_close_df(tickers: list, trading_days: pd.DatetimeIndex, threshold: float = 0.2):
    adj_close_df = pd.DataFrame(index=trading_days)

    for ticker in tickers:
        series = load_price_series(ticker)
        if series is not None:
            adj_close_df[ticker] = series

    return adj_close_df
