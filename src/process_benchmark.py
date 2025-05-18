import pandas as pd

def build_gspc_series(index_path: str, trading_days_path: str) -> pd.Series:
    # Load trading days
    trading_days = pd.read_csv(trading_days_path, parse_dates=['Date'])['Date']

    try:
        # Define expected columns and read index CSV
        cols = ['Date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']
        df = pd.read_csv(index_path, skiprows=3, names=cols, parse_dates=['Date'], index_col='Date')

        # Drop unnecessary column and align with trading days
        df = df.drop(columns=['Price'])
        adj_close = df['Close'].reindex(trading_days)

        return adj_close

    except Exception as e:
        print(f"[ERROR] Failed to process {index_path}: {e}")
        return pd.Series(index=trading_days)
