import os
from config import PORTFOLIO_METRICS_DIR, PORTFOLIO_WEIGHTS_DIR, BASE_STRATEGY_WEIGHTS_DIR
from src.base_strategy_weights import generate_base_strategy_weights

def main():
    print("🚀 Generating base strategy weights using Borda count...")

    os.makedirs(BASE_STRATEGY_WEIGHTS_DIR, exist_ok=True)

    for fname in os.listdir(PORTFOLIO_METRICS_DIR):
        if fname.endswith(".pkl"):
            # Expecting filenames like: portfolio_metrics_annual_1yr.pkl
            print(f"🔍 Processing {fname}...")

            parts = fname.replace(".pkl", "").split('_')
            frequency = parts[2]    # 'annual' or 'quarterly'
            lookback = int(parts[3].replace("yr", ""))  # 1, 2, or 3

            metrics_path = os.path.join(PORTFOLIO_METRICS_DIR, fname)
            weights_path = os.path.join(
                PORTFOLIO_WEIGHTS_DIR,
                f"portfolio_weights_{frequency}_{lookback}yr.pkl"
            )

            save_path = os.path.join(
                BASE_STRATEGY_WEIGHTS_DIR,
                f"base_strategy_weights_{frequency}_{lookback}yr.pkl"
            )

            generate_base_strategy_weights(
                metrics_path=metrics_path,
                weights_path=weights_path,
                save_path=save_path
            )

    print("✅ Finished generating base strategy weights.")

if __name__ == "__main__":
    main()
