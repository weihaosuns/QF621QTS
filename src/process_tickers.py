import pandas as pd

def extract_ticker_list(raw_filepath: str) -> list:
    df = pd.read_csv(raw_filepath)
    return df["Symbol"].tolist()

def save_processed_ticker_list(tickers: list, filepath: str):
    df = pd.DataFrame(tickers, columns=["Symbol"])
    df.to_csv(filepath, index=False)
