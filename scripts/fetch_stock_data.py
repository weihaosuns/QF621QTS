import os
from config import PROCESSED_TICKERS_CSV, RAW_STOCK_DIR, START_DATE, END_DATE
from src.load_stock_data import ensure_dir_exists, download_stock_data, save_stock_data, load_processed_tickers

def main():
    ensure_dir_exists(RAW_STOCK_DIR)

    tickers = load_processed_tickers(PROCESSED_TICKERS_CSV)

    for i, ticker in enumerate(tickers, 1):
        filepath = os.path.join(RAW_STOCK_DIR, f"{ticker}.csv")
        if os.path.exists(filepath):
            print(f"{i}/{len(tickers)} [SKIP] {ticker} data exists.")
            continue

        print(f"{i}/{len(tickers)} Downloading {ticker} ...")
        df = download_stock_data(ticker, START_DATE, END_DATE)

        if df is not None and not df.empty:
            save_stock_data(df, filepath)
            print(f"[SAVED] {ticker} → {filepath}")
        else:
            print(f"[WARN] No data for {ticker}")

if __name__ == "__main__":
    main()
