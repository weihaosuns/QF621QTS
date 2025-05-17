import pandas as pd

def process_trading_days(raw_filepath: str) -> pd.DataFrame:
    df = pd.read_csv(raw_filepath, parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.day_name()
    return df

def save_processed_trading_days(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)
