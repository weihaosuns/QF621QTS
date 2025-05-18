import os
import pickle
import pandas as pd
import numpy as np

def convert_to_dollar_neutral(weights_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert PCA component weights to dollar-neutral long-short portfolio weights
    for each principal component (PC).
    """
    neutral_weights = pd.DataFrame(index=weights_df.index, columns=weights_df.columns)

    for pc in weights_df.index:
        w = weights_df.loc[pc].copy()
        w = w.replace([np.inf, -np.inf], np.nan).fillna(0.0)

        long_mask = w > 0
        short_mask = w < 0

        long_sum = w[long_mask].sum()
        short_sum = -w[short_mask].sum()

        if long_sum > 0:
            w[long_mask] = w[long_mask] / long_sum * 0.5
        else:
            w[long_mask] = 0

        if short_sum > 0:
            w[short_mask] = w[short_mask] / short_sum * 0.5
        else:
            w[short_mask] = 0

        neutral_weights.loc[pc] = w

    return neutral_weights

def run_portfolio_weights_conversion(pca_weights_dir: str, portfolio_weights_dir: str):
    os.makedirs(portfolio_weights_dir, exist_ok=True)

    for fname in os.listdir(pca_weights_dir):
        if fname.endswith(".pkl"):
            fpath = os.path.join(pca_weights_dir, fname)
            print(f"⚙️ Processing {fname}...")

            with open(fpath, "rb") as f:
                pca_weights = pickle.load(f)  # Dict[pd.Timestamp, pd.DataFrame]

            portfolio_weights = {
                date: convert_to_dollar_neutral(weights)
                for date, weights in pca_weights.items()
            }

            save_name = fname.replace("pca_weights", "portfolio_weights")
            save_path = os.path.join(portfolio_weights_dir, save_name)

            with open(save_path, "wb") as f:
                pickle.dump(portfolio_weights, f)

            print(f"✅ Saved dollar-neutral portfolio weights to {save_path}")
