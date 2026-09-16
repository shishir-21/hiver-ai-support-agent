import pandas as pd


INPUT_FILE = "data/golden/llm_reply_judgments.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    score_columns = [
        "relevance",
        "helpfulness",
        "groundedness",
        "safety",
        "clarity",
        "overall",
    ]

    print("Total judged replies:", len(df))

    print("\nAverage scores:")

    for column in score_columns:
        print(
            f"{column}: "
            f"{df[column].astype(float).mean():.2f}"
        )

    print("\nScore distribution for overall:")

    print(
        df["overall"]
        .astype(float)
        .value_counts()
        .sort_index()
    )

    print("\nOverall score percentages:")

    percentages = (
        df["overall"]
        .astype(float)
        .value_counts(normalize=True)
        .sort_index()
        * 100
    )

    for score, percentage in percentages.items():
        print(
            f"{score}: {percentage:.1f}%"
        )


if __name__ == "__main__":
    main()
    