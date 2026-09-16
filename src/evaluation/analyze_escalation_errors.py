import pandas as pd


INPUT_FILE = "data/golden/escalation_predictions.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    missed = df[
        (df["human_escalation"] == "escalate")
        & (df["predicted_escalation"] == "auto_handle")
    ]

    false_escalations = df[
        (df["human_escalation"] == "auto_handle")
        & (df["predicted_escalation"] == "escalate")
    ]

    print("\nEscalation Error Analysis")
    print("=========================")

    print(
        f"\nMissed escalations: {len(missed)}"
    )

    print(
        f"False escalations: {len(false_escalations)}"
    )

    print("\n--- Missed Escalations ---")

    for i, (_, row) in enumerate(missed.iterrows(), 1):

        print(f"\n{i}.")
        print(
            f"ID: {row['customer_tweet_id']}"
        )
        print(
            f"Customer: {row['customer_text']}"
        )
        print(
            f"Reason: {row['reason']}"
        )

    print("\n--- False Escalations ---")

    for i, (_, row) in enumerate(
        false_escalations.iterrows(),
        1,
    ):

        print(f"\n{i}.")
        print(
            f"ID: {row['customer_tweet_id']}"
        )
        print(
            f"Customer: {row['customer_text']}"
        )
        print(
            f"Reason: {row['reason']}"
        )


if __name__ == "__main__":
    main()
    