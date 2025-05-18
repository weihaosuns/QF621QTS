import os
import pandas as pd
from config import PROCESSED_PCA_RETURNS_CSV, PROCESSED_REBALANCE_DATES_CSV, PROCESSED_DATA_DIR
from src.pca_weights import run_rolling_pca_weights

def main():
    print("📂 Loading processed PCA returns...")
    returns_df = pd.read_csv(PROCESSED_PCA_RETURNS_CSV, index_col=0, parse_dates=True)

    print("📅 Loading rebalance dates...")
    rebalance_dates = pd.read_csv(PROCESSED_REBALANCE_DATES_CSV, parse_dates=['rebalance_date'])
    rebalance_dates = rebalance_dates['rebalance_date']

    pca_weights_dir = os.path.join(PROCESSED_DATA_DIR, "pca_weights")
    os.makedirs(pca_weights_dir, exist_ok=True)

    returns_start_date = returns_df.index.min()

    # Annual PCA weights (only March rebalance)
    annual_rebalance_dates = rebalance_dates[rebalance_dates.dt.month == 3]
    print(f"🔄 Running Annual PCA weights on {len(annual_rebalance_dates)} rebalance dates")

    for lookback in [1, 2, 3]:
        run_rolling_pca_weights(
            returns_df,
            annual_rebalance_dates,
            lookback=lookback,
            frequency="annual",
            save_dir=pca_weights_dir,
            returns_start_date=returns_start_date
        )

    # Quarterly PCA weights (all rebalance dates)
    print(f"🔄 Running Quarterly PCA weights on {len(rebalance_dates)} rebalance dates")

    for lookback in [1, 2, 3]:
        run_rolling_pca_weights(
            returns_df,
            rebalance_dates,
            lookback=lookback,
            frequency="quarterly",
            save_dir=pca_weights_dir,
            returns_start_date=returns_start_date
        )

if __name__ == "__main__":
    main()
