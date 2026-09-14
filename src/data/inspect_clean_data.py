import json
import random
from pathlib import Path


DATA_PATH = Path("data/processed/amazon_pairs_en.jsonl")


def main():
    print("=" * 70)
    print("INSPECT CLEAN AMAZONHELP DATA")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"File not found: {DATA_PATH}")
        return

    records = []

    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            records.append(json.loads(line))

    print(f"\nTotal records: {len(records):,}")

    if not records:
        print("No records found.")
        return

    # Check duplicate customer messages.
    customer_texts = [
        record["customer_text"]
        for record in records
    ]

    unique_customer_texts = set(customer_texts)

    print(
        f"Unique customer messages: "
        f"{len(unique_customer_texts):,}"
    )

    print(
        f"Duplicate customer messages: "
        f"{len(customer_texts) - len(unique_customer_texts):,}"
    )

    # Check remaining @mentions.
    mentions = sum(
        "@" in record["customer_text"]
        or "@" in record["support_text"]
        for record in records
    )

    print(f"Records containing @ symbol: {mentions:,}")

    # Text length statistics.
    customer_lengths = [
        len(record["customer_text"])
        for record in records
    ]

    support_lengths = [
        len(record["support_text"])
        for record in records
    ]

    print(
        f"\nAverage customer message length: "
        f"{sum(customer_lengths) / len(customer_lengths):.1f}"
    )

    print(
        f"Average support response length: "
        f"{sum(support_lengths) / len(support_lengths):.1f}"
    )
    
    # Inspect remaining @ symbols.
    print("\nExamples containing @ symbol:")
    print("-" * 70)

    at_records = [
        record
        for record in records
        if "@" in record["customer_text"]
        or "@" in record["support_text"]
    ]

    for i, record in enumerate(at_records[:20], start=1):
        print(f"\nExample {i}")

        print("Customer:")
        print(record["customer_text"])

        print("\nAmazonHelp:")
        print(record["support_text"])

        print("-" * 70)

    # Random examples.
    print("\nRandom sample conversations:")
    print("-" * 70)

    random.seed(42)

    sample_size = min(10, len(records))
    samples = random.sample(records, sample_size)

    for i, record in enumerate(samples, start=1):

        print(f"\nExample {i}")

        print("\nCustomer:")
        print(record["customer_text"])

        print("\nAmazonHelp:")
        print(record["support_text"])

        print("-" * 70)

    print("\nInspection complete.")


if __name__ == "__main__":
    main()
    