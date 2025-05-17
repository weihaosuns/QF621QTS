import os
import pandas as pd
from config import (
    PROCESSED_TICKERS_CSV,
    PROCESSED_TRADING_DAYS_CSV,
    PROCESSED_DATA_DIR
)
from src.process_stock_data import (
    load_ticker_list,
    load_trading_days,
    adj_close_df
)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    print("Loading tickers and trading days...")
    tickers = load_ticker_list(PROCESSED_TICKERS_CSV)
    trading_days = load_trading_days(PROCESSED_TRADING_DAYS_CSV)

    print(f"Building adjusted close DataFrame from {len(tickers)} tickers...")

    df = adj_close_df(tickers, trading_days)

    print(f"\nDropped {len(dropped)} tickers with >20% missing values:")
    for ticker in dropped:
        print(f" - {ticker}")

    print(f"\nFinal shape after cleaning: {df.shape}")

    ensure_dir(PROCESSED_DATA_DIR)
    out_path = os.path.join(PROCESSED_DATA_DIR, "prices_df.csv")
    df.to_csv(out_path)
    print(f"Saved cleaned adjusted close data to: {out_path}")

if __name__ == "__main__":
    main()
