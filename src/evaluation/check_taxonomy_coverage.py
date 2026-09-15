import pandas as pd

INPUT_FILE = "data/golden/amazon_golden_200.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 70)
    print("TAXONOMY COVERAGE CHECK")
    print("=" * 70)

    print(f"\nTotal golden examples: {len(df)}")

    # These are only inspection phrases.
    # They do NOT assign labels automatically.
    categories = {
        "delivery_issue": [
            "delivery",
            "delivered",
            "package",
            "parcel",
            "shipping",
            "shipped",
            "carrier",
            "arrive",
            "arrived",
            "tracking",
            "where is my",
        ],
        "order_or_product_issue": [
            "wrong item",
            "wrong product",
            "damaged",
            "broken",
            "missing item",
            "defective",
            "product",
            "item",
        ],
        "return_or_refund": [
            "refund",
            "return",
            "money back",
            "returned",
        ],
        "payment_or_amazon_pay": [
            "payment",
            "charged",
            "charge",
            "amazon pay",
            "debit",
            "credit card",
            "billing",
        ],
        "account_access_or_security": [
            "account",
            "login",
            "log in",
            "password",
            "hacked",
            "locked",
            "security",
        ],
        "prime_membership_or_benefit": [
            "prime",
            "membership",
            "prime member",
            "prime membership",
        ],
        "feedback_or_praise": [
            "thank",
            "thanks",
            "great service",
            "love amazon",
            "worst customer service",
            "amazing",
            "awesome",
        ],
    }

    text = df["customer_text"].fillna("").str.lower()

    matched_counts = {}

    for category, phrases in categories.items():
        mask = text.apply(
            lambda x: any(phrase in x for phrase in phrases)
        )

        matched_counts[category] = int(mask.sum())

    print("\nPotential thematic coverage:")
    print("-" * 70)

    for category, count in matched_counts.items():
        print(f"{category:35} {count}")

    # Messages that do not contain any obvious thematic phrase.
    all_masks = []

    for phrases in categories.values():
        mask = text.apply(
            lambda x: any(phrase in x for phrase in phrases)
        )
        all_masks.append(mask)

    any_match = all_masks[0].copy()

    for mask in all_masks[1:]:
        any_match = any_match | mask

    unmatched = df[~any_match]

    print("\nMessages without an obvious thematic phrase:")
    print("-" * 70)
    print(f"Count: {len(unmatched)}")

    for _, row in unmatched.iterrows():
        print("-" * 70)
        print(f"Customer ID: {row['customer_tweet_id']}")
        print(f"Customer: {row['customer_text']}")
        print(f"Support:  {row['support_text']}")

    print("\nTaxonomy coverage check complete.")


if __name__ == "__main__":
    main()
    