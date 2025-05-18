import os
from config import PORTFOLIO_WEIGHTS_DIR, PORTFOLIO_METRICS_DIR
from src.performance_metrics import run_performance_metrics_calculation

def main():
    print("🚀 Starting portfolio performance metrics calculation...")

    for fname in os.listdir(PORTFOLIO_WEIGHTS_DIR):
        if fname.endswith(".pkl"):
            # Expecting filenames like 'portfolio_weights_annual_1yr.pkl'
            print(f"🔍 Processing {fname}...")

            parts = fname.replace(".pkl", "").split('_')
            # parts example: ['portfolio', 'weights', 'annual', '1yr']
            frequency = parts[2]
            lookback_str = parts[3]
            lookback = int(lookback_str.replace("yr", ""))

            weights_path = os.path.join(PORTFOLIO_WEIGHTS_DIR, fname)
            run_performance_metrics_calculation(weights_path, lookback, frequency, PORTFOLIO_METRICS_DIR)

if __name__ == "__main__":
    main()
