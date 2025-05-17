import os
from src.process_tickers import extract_ticker_list, save_processed_ticker_list
from config import RAW_TICKERS_CSV, PROCESSED_TICKERS_CSV, PROCESSED_DATA_DIR

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir_exists(PROCESSED_DATA_DIR)
    tickers = extract_ticker_list(RAW_TICKERS_CSV)
    save_processed_ticker_list(tickers, PROCESSED_TICKERS_CSV)
    print(f"Processed tickers saved to {PROCESSED_TICKERS_CSV}")

if __name__ == "__main__":
    main()
