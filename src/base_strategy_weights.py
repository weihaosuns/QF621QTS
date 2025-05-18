import os
import pickle
import pandas as pd

# Metrics where higher is better
POSITIVE_METRICS = [
    "Annualized Return", "Sharpe Ratio", "Sortino Ratio",
    "Alpha", "Treynor Ratio", "Information Ratio", "Calmar Ratio"
]
# Metrics where lower is better
NEGATIVE_METRICS = ["Volatility", "Beta", "Max Drawdown"]


def borda_rank(df):
    rank_df = pd.DataFrame(index=df.index)
    for col in df.columns:
        if col in POSITIVE_METRICS:
            rank_df[col] = df[col].rank(ascending=False, method='min')
        elif col in NEGATIVE_METRICS:
            rank_df[col] = df[col].rank(ascending=True, method='min')
    return rank_df.sum(axis=1)  # Borda score


def generate_base_strategy_weights(metrics_path: str, weights_path: str, save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(metrics_path, "rb") as f:
        all_metrics = pickle.load(f)

    with open(weights_path, "rb") as f:
        all_weights = pickle.load(f)

    base_strategy_weights = {}
    selected_pcs_by_date = {}  # ← to store selected PCs

    for date in all_metrics:
        metrics_df = all_metrics[date]  # PCs x metrics
        weights_df = all_weights[date]  # PCs x stocks

        borda_scores = borda_rank(metrics_df)
        max_score = borda_scores.max()
        top_pcs = borda_scores[borda_scores == max_score].index

        selected_weights = weights_df.loc[top_pcs]
        avg_weights = selected_weights.mean(axis=0)
        base_strategy_weights[date] = avg_weights

        selected_pcs_by_date[date] = list(top_pcs)
        # Uncomment to print which PCs were selected
        print(f"{date.date()}: selected PCs = {list(top_pcs)}")

    with open(save_path, "wb") as f:
        pickle.dump(base_strategy_weights, f)

    print(f"✅ Base strategy weights saved to {save_path}")

    # Optionally return selected PCs per date if used interactively
    return selected_pcs_by_date
