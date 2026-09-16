import pandas as pd


PREDICTIONS_FILE = "data/golden/llm_intent_predictions.csv"


def main():
    df = pd.read_csv(PREDICTIONS_FILE, dtype=str).fillna("")

    errors = df[
        df["true_intent"] != df["predicted_intent"]
    ].copy()

    print(f"Total examples: {len(df)}")
    print(f"Correct predictions: {len(df) - len(errors)}")
    print(f"Incorrect predictions: {len(errors)}")

    print("\nError pairs:")
    print(
        errors.groupby(
            ["true_intent", "predicted_intent"]
        ).size().sort_values(ascending=False)
    )

    print("\nSample errors:\n")

    for _, row in errors.head(20).iterrows():
        print("=" * 70)
        print("Customer:", row["customer_text"])
        print("True intent:", row["true_intent"])
        print("Predicted:", row["predicted_intent"])
        print("Reason:", row["reason"])


if __name__ == "__main__":
    main()
    