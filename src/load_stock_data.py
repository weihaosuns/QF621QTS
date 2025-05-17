import os
import yfinance as yf
import pandas as pd

def ensure_dir_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    return df

def save_stock_data(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath)

def load_processed_tickers(csv_path: str) -> list:
    df = pd.read_csv(csv_path)
    return df["Symbol"].tolist()


