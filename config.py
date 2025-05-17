import os
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Paths for tickers
RAW_TICKERS_CSV = os.path.join(RAW_DATA_DIR, "sp500_tickers.csv")
PROCESSED_TICKERS_CSV = os.path.join(PROCESSED_DATA_DIR, "sp500_tickers_processed.csv")

# Paths for trading days
RAW_TRADING_DAYS_CSV = os.path.join(RAW_DATA_DIR, "us_trading_days.csv")
PROCESSED_TRADING_DAYS_CSV = os.path.join(PROCESSED_DATA_DIR, "us_trading_days_processed.csv")

# Paths for prices
RAW_STOCK_DIR = os.path.join(RAW_DATA_DIR, "stock")  # if multiple files or big files
PROCESSED_STOCK_CSV = os.path.join(PROCESSED_DATA_DIR, "prices_df.csv")

# Dates for downloading prices
START_DATE = "2000-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")
