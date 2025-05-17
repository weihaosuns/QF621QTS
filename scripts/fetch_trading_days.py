import os
from config import RAW_TRADING_DAYS_CSV, RAW_DATA_DIR, START_DATE, END_DATE
from src.load_trading_days import download_us_trading_days, save_raw_trading_days

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir_exists(RAW_DATA_DIR)
    df = download_us_trading_days(START_DATE, END_DATE)
    save_raw_trading_days(df, RAW_TRADING_DAYS_CSV)
    print(f"Raw US trading days saved to {RAW_TRADING_DAYS_CSV}")

if __name__ == "__main__":
    main()
