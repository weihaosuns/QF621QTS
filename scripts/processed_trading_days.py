import os
from config import RAW_TRADING_DAYS_CSV, PROCESSED_TRADING_DAYS_CSV, PROCESSED_DATA_DIR
from src.process_trading_days import process_trading_days, save_processed_trading_days

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir_exists(PROCESSED_DATA_DIR)
    df = process_trading_days(RAW_TRADING_DAYS_CSV)
    save_processed_trading_days(df, PROCESSED_TRADING_DAYS_CSV)
    print(f"Processed US trading days saved to {PROCESSED_TRADING_DAYS_CSV}")

if __name__ == "__main__":
    main()
