import os
from config import PROCESSED_STOCK_CSV, PROCESSED_PCA_RETURNS_CSV
from src.process_pca_data import preprocess_for_pca

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    print("🔄 Preprocessing S&P 500 returns for PCA ...")
    df = preprocess_for_pca(PROCESSED_STOCK_CSV)
    print(f"✅ Final shape: {df.shape}")

    ensure_dir_exists(PROCESSED_PCA_RETURNS_CSV)
    df.to_csv(PROCESSED_PCA_RETURNS_CSV)
    print(f"💾 Saved to: {PROCESSED_PCA_RETURNS_CSV}")

if __name__ == "__main__":
    main()
