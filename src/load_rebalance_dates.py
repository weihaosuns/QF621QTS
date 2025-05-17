import pandas as pd
from datetime import datetime

def load_rebalance_dates(trading_days_path: str, rebalance_dates_path: str):
    # Load processed US trading days, assuming column 'Date' or 'date'
    trading_days_df = pd.read_csv(trading_days_path, parse_dates=['Date'])
    trading_days = trading_days_df['Date'].sort_values().reset_index(drop=True)

    # Get all years covered by trading_days
    years = trading_days.dt.year.unique()

    # Earnings dates per year
    earnings_dates = []
    for year in years:
        earnings_dates += [
            datetime(year, 3, 1),
            datetime(year, 5, 10),
            datetime(year, 8, 9),
            datetime(year, 11, 9),
        ]

    rebalance_dates = []
    for edate in earnings_dates:
        # Find the trading day equal or just after edate
        # If edate not in trading days, pick the next trading day
        candidates = trading_days[trading_days >= edate]
        if not candidates.empty:
            rebalance_dates.append(candidates.iloc[0])

    rebalance_df = pd.DataFrame({'rebalance_date': rebalance_dates})
    rebalance_df.to_csv(rebalance_dates_path, index=False)
    print(f"Saved {len(rebalance_df)} rebalance dates to {rebalance_dates_path}")

    return rebalance_df
