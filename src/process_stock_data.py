import os
import pandas as pd

def build_adjclose_dataframe(stock_dir: str, trading_days_path: str) -> pd.DataFrame:
    # Use correct column name "Date" (capital D)
    trading_days = pd.read_csv(trading_days_path, parse_dates=['Date'])['Date']

    all_prices = pd.DataFrame(index=trading_days)

    for file in os.listdir(stock_dir):
        if not file.endswith('.csv'):
            continue

        ticker = file.replace(".csv", "")
        path = os.path.join(stock_dir, file)

        try:
            cols = ['Date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']
            df = pd.read_csv(path, skiprows=3, names=cols, parse_dates=['Date'], index_col='Date')
            df = df.drop(columns=['Price'])
            adj_close = df['Close'].reindex(trading_days)
            all_prices[ticker] = adj_close
        except Exception as e:
            print(f"[WARN] Skipping {ticker} due to error: {e}")

    return all_prices
