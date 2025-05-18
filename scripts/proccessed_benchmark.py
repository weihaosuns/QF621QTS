import os
from config import RAW_GSPC_CSV, PROCESSED_TRADING_DAYS_CSV, PROCESSED_GSPC_CSV
from src.process_benchmark import build_gspc_series

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    print("📈 Building ^GSPC Adjusted Close Series ...")
    series = build_gspc_series(RAW_GSPC_CSV, PROCESSED_TRADING_DAYS_CSV)
    print(f"✅ Final Series length: {series.shape[0]}")

    ensure_dir_exists(PROCESSED_GSPC_CSV)
    series.to_csv(PROCESSED_GSPC_CSV, header=["GSPC"])
    print(f"💾 Saved to: {PROCESSED_GSPC_CSV}")

if __name__ == "__main__":
    main()
