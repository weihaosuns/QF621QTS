import pandas as pd
import pandas_market_calendars as mcal

def download_us_trading_days(start_date: str, end_date: str) -> pd.DataFrame:
    nyse = mcal.get_calendar("NYSE")
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)
    dates_df = schedule.index.to_frame(index=False, name="Date")
    return dates_df

def save_raw_trading_days(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

def load_raw_trading_days(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=["Date"])
