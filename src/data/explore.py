from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")


def main():
    print("=" * 60)
    print("HIVER AI SUPPORT AGENT - DATASET EXPLORATION")
    print("=" * 60)

    # Check that the dataset exists
    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        return

    print(f"\nDataset: {DATA_PATH}")
    print(f"File size: {DATA_PATH.stat().st_size / (1024 ** 2):.2f} MB")

    # Read only the first few rows for initial inspection
    df = pd.read_csv(DATA_PATH, nrows=5)

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nFirst 5 rows:")
    print(df.to_string(index=False))

    print("\nData types:")
    print(df.dtypes)

    print("\nInitial exploration complete.")


if __name__ == "__main__":
    main()
