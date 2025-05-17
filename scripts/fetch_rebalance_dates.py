from config import PROCESSED_TRADING_DAYS_CSV, PROCESSED_REBALANCE_DATES_CSV
from src.load_rebalance_dates import load_rebalance_dates

def main():
    df = load_rebalance_dates(PROCESSED_TRADING_DAYS_CSV, PROCESSED_REBALANCE_DATES_CSV)
    print(df.head())

if __name__ == "__main__":
    main()
