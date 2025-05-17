import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_for_pca(filepath: str, missing_threshold: float = 0.1) -> pd.DataFrame:
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

    # 1. Drop tickers with >10% missing
    missing_ratio = df.isna().mean()
    dropped_tickers = missing_ratio[missing_ratio > missing_threshold].index.tolist()
    print(f"🧹 Dropped {len(dropped_tickers)} tickers due to >{int(missing_threshold*100)}% missing data.")
    df = df.drop(columns=dropped_tickers)

    # 2. Forward-fill remaining missing values
    df = df.ffill()

    # 3. Compute log returns
    returns = np.log(df / df.shift(1))

    # 4. Drop rows with any NaNs
    returns.dropna(inplace=True)

    # 5. Standardize the data to avoid high volatility stocks dominating the weights
    scaler = StandardScaler()
    returns_std = pd.DataFrame(scaler.fit_transform(returns), index=returns.index, columns=returns.columns)

    return returns_std




