import json
import random
from pathlib import Path


INPUT_FILE = Path("data/processed/amazon_pairs_en.jsonl")


THEMES = {
    "delivery": [
        "where is my",
        "out for delivery",
        "not received",
        "be delivered",
        "my package",
        "my order",
    ],
    "prime": [
        "amazon prime",
        "prime membership",
        "pay for prime",
        "amazon prime",
    ],
    "account": [
        "my account",
        "account",
        "not able to",
    ],
    "payment": [
        "amazon pay",
        "pay",
        "charged",
        "payment",
    ],
    "feedback": [
        "thank you",
        "you guys are",
        "customer service is",
    ],
}


def load_messages():
    messages = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            messages.append(record["customer_text"])

    return messages


def main():
    messages = load_messages()

    print(f"Loaded messages: {len(messages):,}")

    for theme, phrases in THEMES.items():
        print("\n" + "=" * 70)
        print(f"THEME: {theme.upper()}")
        print("=" * 70)

        matched = []

        for message in messages:
            text = message.lower()

            if any(phrase in text for phrase in phrases):
                matched.append(message)

        print(f"Matched messages: {len(matched):,}")

        sample_size = min(15, len(matched))

        for message in random.sample(matched, sample_size):
            print(f"- {message}")


if __name__ == "__main__":
    main()
    