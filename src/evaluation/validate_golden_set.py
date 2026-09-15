import pandas as pd
from langdetect import detect, LangDetectException


INPUT_FILE = "data/golden/amazon_golden_200.csv"


def detect_language(text):
    try:
        return detect(str(text))
    except LangDetectException:
        return "unknown"


def main():
    df = pd.read_csv(INPUT_FILE)

    # Detect language on both sides of the support pair.
    df["customer_language"] = df["customer_text"].apply(
        detect_language
    )

    df["support_language"] = df["support_text"].apply(
        detect_language
    )

    print("\nCustomer language distribution:")
    print(df["customer_language"].value_counts())

    print("\nSupport language distribution:")
    print(df["support_language"].value_counts())

    # A pair is valid only when BOTH customer and support messages
    # are detected as English.
    invalid = df[
        (df["customer_language"] != "en")
        | (df["support_language"] != "en")
    ]

    print(f"\nTotal golden examples: {len(df)}")
    print(f"Invalid language pairs: {len(invalid)}")
    print(f"Valid English pairs: {len(df) - len(invalid)}")

    if not invalid.empty:
        print("\nInvalid examples:")

        for _, row in invalid.iterrows():
            print("-" * 70)
            print(f"Customer language: {row['customer_language']}")
            print(f"Support language:  {row['support_language']}")
            print(f"Customer: {row['customer_text']}")
            print(f"Support:  {row['support_text']}")

    print("\nValidation complete.")


if __name__ == "__main__":
    main()
    