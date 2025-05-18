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

# Paths for stock price files and combined dataframe
RAW_STOCK_DIR = os.path.join(RAW_DATA_DIR, "stock")
PROCESSED_STOCK_CSV = os.path.join(PROCESSED_DATA_DIR, "all_snp_prices.csv")

# Path for PCA-ready returns
PROCESSED_PCA_RETURNS_CSV = os.path.join(PROCESSED_DATA_DIR, "processed_pca_returns.csv")

# Path for Rebalance Dates
PROCESSED_REBALANCE_DATES_CSV = os.path.join(PROCESSED_DATA_DIR, "rebalance_dates.csv")

# Paths for PCA weights
PCA_WEIGHTS_DIR = os.path.join(PROCESSED_DATA_DIR, "pca_weights")

# Path for Portfolio weights
PORTFOLIO_WEIGHTS_DIR = os.path.join(PROCESSED_DATA_DIR, "portfolio_weights")

# Path for raw and processed GSPC data
RAW_GSPC_CSV = os.path.join(RAW_DATA_DIR, "^GSPC.csv")
PROCESSED_GSPC_CSV = os.path.join(PROCESSED_DATA_DIR, "gspc_adjclose.csv")

# Path for Portfolio metrics
PORTFOLIO_METRICS_DIR = os.path.join(PROCESSED_DATA_DIR, "portfolio_metrics")

# Path for Base Strategy weights
BASE_STRATEGY_WEIGHTS_DIR = os.path.join(PROCESSED_DATA_DIR, "base_strategy_weights")

# Dates for downloading prices
START_DATE = "2000-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")
