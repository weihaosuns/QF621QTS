import os
from src.load_tickers import download_sp500_tickers, save_raw_tickers
from config import RAW_TICKERS_CSV, RAW_DATA_DIR

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir_exists(RAW_DATA_DIR)
    df = download_sp500_tickers()
    save_raw_tickers(df, RAW_TICKERS_CSV)
    print(f"Raw tickers saved to {RAW_TICKERS_CSV}")

if __name__ == "__main__":
    main()
