import os
import time
from config import PROCESSED_TICKERS_CSV, RAW_STOCK_DIR, START_DATE, END_DATE
from src.load_stock_data import ensure_dir_exists, download_stock_data, save_stock_data, load_processed_tickers

BATCH_SIZE = 5
WAIT_TIME = 600  # 10 minutes in seconds

def main():
    ensure_dir_exists(RAW_STOCK_DIR)
    tickers = load_processed_tickers(PROCESSED_TICKERS_CSV)
    total = len(tickers)

    i = 0
    while i < total:
        batch = tickers[i:i + BATCH_SIZE]
        print(f"\n📦 Batch {i // BATCH_SIZE + 1}: {batch}")

        for j, ticker in enumerate(batch, i + 1):
            filepath = os.path.join(RAW_STOCK_DIR, f"{ticker}.csv")
            if os.path.exists(filepath):
                print(f"{j}/{total} [SKIP] {ticker} data exists.")
                continue

            print(f"{j}/{total} Downloading {ticker} ...")
            df = download_stock_data(ticker, START_DATE, END_DATE)

            if df is not None and not df.empty:
                save_stock_data(df, filepath)
                print(f"[SAVED] {ticker} → {filepath}")
            else:
                print(f"[WARN] No data for {ticker}")

        i += BATCH_SIZE
        if i < total:
            print(f"\n⏱ Waiting {WAIT_TIME // 60} minutes before next batch...")
            time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
