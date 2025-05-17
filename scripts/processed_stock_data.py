import os
from config import RAW_STOCK_DIR, PROCESSED_TRADING_DAYS_CSV, PROCESSED_STOCK_CSV
from src.process_stock_data import build_adjclose_dataframe

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    print("📈 Building S&P 500 Close Price DataFrame ...")
    df = build_adjclose_dataframe(RAW_STOCK_DIR, PROCESSED_TRADING_DAYS_CSV)
    print(f"✅ Final DataFrame shape: {df.shape}")

    ensure_dir_exists(PROCESSED_STOCK_CSV)
    df.to_csv(PROCESSED_STOCK_CSV)
    print(f"💾 Saved to: {PROCESSED_STOCK_CSV}")

if __name__ == "__main__":
    main()
