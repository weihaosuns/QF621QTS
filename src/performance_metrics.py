import os
import pickle
import pandas as pd
import numpy as np
from config import PROCESSED_STOCK_CSV, PROCESSED_GSPC_CSV, PORTFOLIO_METRICS_DIR

def calculate_performance_metrics(portfolio_returns, benchmark_returns):
    """
    Calculate various performance metrics for portfolio returns compared to benchmark returns.

    Parameters:
    - portfolio_returns: pd.Series, daily returns indexed by date
    - benchmark_returns: pd.Series, daily benchmark returns indexed by date (same period)

    Returns: dict of metrics
    """
    excess_returns = portfolio_returns - benchmark_returns

    # Basic stats
    mean_return = portfolio_returns.mean() * 252
    vol = portfolio_returns.std() * np.sqrt(252)

    # Sharpe Ratio (using risk-free rate = 0)
    sharpe_ratio = mean_return / vol if vol != 0 else np.nan

    # Sortino Ratio (only downside volatility)
    negative_returns = portfolio_returns[portfolio_returns < 0]
    downside_std = negative_returns.std() * np.sqrt(252)
    sortino_ratio = mean_return / downside_std if downside_std != 0 else np.nan

    # Beta and Alpha (regression)
    if len(portfolio_returns) >= 2 and len(benchmark_returns) >= 2:
        # Check if they are Series/arrays and not scalars
        if isinstance(portfolio_returns, (pd.Series, np.ndarray)) and isinstance(benchmark_returns, (pd.Series, np.ndarray)):
            cov = np.cov(portfolio_returns, benchmark_returns)
            if cov.shape == (2,2) and cov[1,1] != 0:
                beta = cov[0,1] / cov[1,1]
                alpha = mean_return - beta * benchmark_returns.mean() * 252
            else:
                beta = np.nan
                alpha = np.nan
        else:
            beta = np.nan
            alpha = np.nan
    else:
        beta = np.nan
        alpha = np.nan

    # Treynor Ratio = (Return - Rf) / Beta
    treynor_ratio = mean_return / beta if beta not in [0, np.nan] else np.nan

    # Max Drawdown
    cumulative = (1 + portfolio_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # Information Ratio = (Portfolio excess return) / Tracking error
    tracking_error = excess_returns.std() * np.sqrt(252)
    information_ratio = excess_returns.mean() * 252 / tracking_error if tracking_error != 0 else np.nan

    # Calmar Ratio = Annualized return / max drawdown (absolute)
    calmar_ratio = mean_return / abs(max_drawdown) if max_drawdown != 0 else np.nan

    metrics = {
        "Annualized Return": mean_return,
        "Volatility": vol,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "Beta": beta,
        "Alpha": alpha,
        "Treynor Ratio": treynor_ratio,
        "Max Drawdown": max_drawdown,
        "Information Ratio": information_ratio,
        "Calmar Ratio": calmar_ratio
    }

    return metrics


def run_performance_metrics_calculation(
    portfolio_weights_path: str,
    lookback_years: int,
    frequency: str,
    save_dir: str = PORTFOLIO_METRICS_DIR
):
    """
    Calculate portfolio performance metrics for all dates and PCs,
    using daily returns capped by lookback years, benchmark included.

    Parameters:
    - portfolio_weights_path: str, path to portfolio weights pickle file
    - lookback_years: int, lookback window in years
    - frequency: str, 'annual' or 'quarterly'
    - save_dir: str, directory to save output metrics pickle
    """

    os.makedirs(save_dir, exist_ok=True)

    # Load portfolio weights: Dict[date, DataFrame with PCs]
    with open(portfolio_weights_path, "rb") as f:
        portfolio_weights = pickle.load(f)

    # Load daily stock prices and compute daily returns
    prices = pd.read_csv(PROCESSED_STOCK_CSV, index_col=0, parse_dates=True)
    stock_returns = prices.pct_change().dropna(how='all')

    # Load benchmark prices and compute returns
    benchmark_prices = pd.read_csv(PROCESSED_GSPC_CSV, index_col=0, parse_dates=True)
    benchmark_returns = benchmark_prices[benchmark_prices.columns[0]].pct_change().dropna()

    all_metrics = {}

    for date, weights_df in portfolio_weights.items():
        # Determine lookback window for daily returns
        start_date = pd.to_datetime(date) - pd.DateOffset(years=lookback_years)
        end_date = pd.to_datetime(date)

        # Slice returns
        daily_returns_window = stock_returns.loc[start_date:end_date]
        benchmark_returns_window = benchmark_returns.loc[start_date:end_date]

        # Align index to avoid mismatch
        daily_returns_window = daily_returns_window.dropna(axis=1, how='all')  # drop stocks missing in window
        common_dates = daily_returns_window.index.intersection(benchmark_returns_window.index)
        daily_returns_window = daily_returns_window.loc[common_dates]
        benchmark_returns_window = benchmark_returns_window.loc[common_dates]

        metrics_per_pc = {}

        for pc in weights_df.index:
            weights = weights_df.loc[pc]
            # Filter stocks present in daily_returns_window
            common_stocks = daily_returns_window.columns.intersection(weights.index)
            w = weights[common_stocks]

            # Calculate portfolio returns for the PC: weighted sum of daily returns
            portfolio_ret = daily_returns_window[common_stocks].dot(w)
            portfolio_ret = pd.to_numeric(portfolio_ret, errors='coerce')  # <- convert to float, coercing errors to NaN
            portfolio_ret = portfolio_ret.dropna()  # drop NaNs after conversion

            # Calculate metrics
            metrics = calculate_performance_metrics(portfolio_ret, benchmark_returns_window)
            metrics_per_pc[pc] = metrics

        all_metrics[date] = pd.DataFrame(metrics_per_pc).T  # PC as rows

    # Save results
    fname = f"portfolio_metrics_{frequency}_{lookback_years}yr.pkl"
    save_path = os.path.join(save_dir, fname)
    with open(save_path, "wb") as f:
        pickle.dump(all_metrics, f)

    print(f"✅ Saved portfolio metrics for {frequency} {lookback_years}yr at:\n{save_path}")
