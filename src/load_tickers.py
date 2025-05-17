import pandas as pd

def download_sp500_tickers() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(url)[0]
    return df

def save_raw_tickers(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

def load_raw_tickers(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)
