import os
import pickle
import pandas as pd
from sklearn.decomposition import PCA

def filter_rebalance_dates(rebalance_dates, returns_start_date, lookback_years):
    """
    Filter out rebalance dates whose lookback window start is before returns_start_date.

    Parameters:
    - rebalance_dates: iterable of pd.Timestamp or date-like
    - returns_start_date: pd.Timestamp or date-like, start date of returns data
    - lookback_years: int, lookback window in years

    Returns:
    - pd.Series of filtered rebalance dates
    """
    returns_start_date = pd.to_datetime(returns_start_date)
    filtered = []
    for date in rebalance_dates:
        date = pd.to_datetime(date)
        window_start = date - pd.DateOffset(years=lookback_years)
        if window_start >= returns_start_date:
            filtered.append(date)
        else:
            print(f"[INFO] Skipping rebalance date {date.date()} due to insufficient lookback data window.")
    return pd.Series(filtered)

def run_rolling_pca_weights(
    returns_df: pd.DataFrame,
    rebalance_dates: pd.Series,
    lookback: int,
    frequency: str,
    save_dir: str,
    returns_start_date
):
    """
    Calculate PCA weights for all components using rolling lookback windows,
    on given rebalance dates, saving results as pickle.

    Parameters:
    - returns_df: pd.DataFrame, daily returns (index=date, columns=tickers)
    - rebalance_dates: pd.Series of pd.Timestamp, PCA cutoff dates
    - lookback: int, rolling window length in years
    - frequency: str, e.g. 'annual', 'quarterly'
    - save_dir: str, directory to save pickle
    - returns_start_date: pd.Timestamp or str, earliest date returns are available
    """
    os.makedirs(save_dir, exist_ok=True)
    all_weights = {}

    # Filter rebalance dates to ensure lookback window is valid
    filtered_dates = filter_rebalance_dates(rebalance_dates, returns_start_date, lookback)

    for date in filtered_dates:
        start_date = date - pd.DateOffset(years=lookback)
        data_window = returns_df.loc[start_date:date].dropna(axis=1, how='any')

        if data_window.shape[0] < 60:
            print(f"[WARN] Skipping {date.date()} ({lookback}yr) - insufficient data points ({data_window.shape[0]})")
            continue

        n_components = min(data_window.shape[1], data_window.shape[0])
        pca = PCA(n_components=n_components)
        pca.fit(data_window.values)

        weights = pd.DataFrame(
            pca.components_,
            columns=data_window.columns,
            index=[f"PC{i+1}" for i in range(n_components)]
        )

        all_weights[date] = weights

    fname = f"pca_weights_{frequency}_{lookback}yr.pkl"
    save_path = os.path.join(save_dir, fname)
    with open(save_path, "wb") as f:
        pickle.dump(all_weights, f)

    print(f"✅ Saved PCA weights (all components) for {frequency} {lookback}yr at:\n{save_path}")
