import pandas as pd


GOLDEN_FILE = "data/golden/amazon_golden_200_annotated.csv"
PREDICTIONS_FILE = "data/golden/escalation_predictions.csv"


def main():

    golden_df = pd.read_csv(
        GOLDEN_FILE,
        dtype=str,
    ).fillna("")

    predictions_df = pd.read_csv(
        PREDICTIONS_FILE,
        dtype=str,
    ).fillna("")

    # Get the human intent labels from the golden dataset.
    intent_df = golden_df[
        [
            "customer_tweet_id",
            "intent",
        ]
    ]

    # Add intent to escalation predictions.
    df = predictions_df.merge(
        intent_df,
        on="customer_tweet_id",
        how="left",
    )

    missed = df[
        (df["human_escalation"] == "escalate")
        & (df["predicted_escalation"] == "auto_handle")
    ].copy()

    print("\nMissed Escalations by Intent")
    print("============================")

    counts = (
        missed["intent"]
        .value_counts()
        .sort_values(ascending=False)
    )

    print(counts)

    print("\nPercentage of missed escalations:")

    percentages = (
        missed["intent"]
        .value_counts(normalize=True)
        .sort_values(ascending=False)
        * 100
    )

    for intent, percentage in percentages.items():
        print(
            f"{intent}: {percentage:.1f}%"
        )


if __name__ == "__main__":
    main()
    