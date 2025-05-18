# scripts/generate_portfolio_weights.py
import os
from config import PCA_WEIGHTS_DIR, PORTFOLIO_WEIGHTS_DIR
from src.portfolio_weights import run_portfolio_weights_conversion

def main():
    print("🚀 Generating portfolio weights from PCA weights...")
    run_portfolio_weights_conversion(PCA_WEIGHTS_DIR, PORTFOLIO_WEIGHTS_DIR)

if __name__ == "__main__":
    main()