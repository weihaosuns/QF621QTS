import os
import pandas as pd
from sklearn.decomposition import PCA

def run_rolling_pca_weights(
    returns_df: pd.DataFrame,
    rebalance_dates: pd.Series,
    lookback: int,
    frequency: str,
    save_dir: str
):
    """
    Calculate PCA weights for ALL components using rolling lookback windows,
    at given rebalance dates and save as pickle files.

    Parameters:
    - returns_df: pd.DataFrame with returns (index=date, columns=tickers)
    - rebalance_dates: pd.Series or list of pd.Timestamp for PCA cut-off
    - lookback: int, rolling window length in years
    - frequency: str, e.g., 'annual' or 'quarterly'
    - save_dir: str, directory to save pickle files
    """

    os.makedirs(save_dir, exist_ok=True)
    all_weights = {}

    for date in rebalance_dates:
        start_date = date - pd.DateOffset(years=lookback)
        # Select returns window
        data_window = returns_df.loc[start_date:date].dropna(axis=1, how='any')

        if data_window.shape[0] < 60:
            print(f"[WARN] Skipping {date.date()} ({lookback}yr) insufficient data points ({data_window.shape[0]})")
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

    # Save as pickle
    import pickle
    fname = f"pca_weights_{frequency}_{lookback}yr.pkl"
    path = os.path.join(save_dir, fname)
    with open(path, "wb") as f:
        pickle.dump(all_weights, f)

    print(f"✅ Saved PCA weights (all components) for {frequency}, {lookback}yr to:\n{path}")
