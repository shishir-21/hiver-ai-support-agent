from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")


def main():
    print("=" * 70)
    print("HIVER AI SUPPORT AGENT - BRAND ANALYSIS")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        return

    print("\nReading dataset...")

    # We only need the columns required for brand-level analysis.
    df = pd.read_csv(
        DATA_PATH,
        usecols=[
            "tweet_id",
            "author_id",
            "inbound",
            "response_tweet_id",
            "in_response_to_tweet_id",
        ],
    )

    print(f"Total tweets: {len(df):,}")

    # A brand account appears as an author_id on outbound/support tweets.
    support_tweets = df[df["inbound"] == False].copy()

    # Count support tweets for every brand.
    brand_counts = (
        support_tweets["author_id"]
        .value_counts()
        .reset_index()
    )

    brand_counts.columns = ["brand", "support_tweets"]

    print("\nTop 30 brands by number of support tweets:")
    print(brand_counts.head(30).to_string(index=False))

    # Customer tweets
    customer_tweets = df[df["inbound"] == True].copy()

    print("\nCustomer tweets:", f"{len(customer_tweets):,}")
    print("Support tweets:", f"{len(support_tweets):,}")

    print("\nBrand analysis complete.")


if __name__ == "__main__":
    main()
