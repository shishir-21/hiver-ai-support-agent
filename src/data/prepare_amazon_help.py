import json
import re
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")
OUTPUT_PATH = Path("data/processed/amazon_pairs_en.jsonl")

BRAND = "AmazonHelp"


# Common English words that frequently occur in support conversations.
ENGLISH_WORDS = {
    "the",
    "is",
    "my",
    "to",
    "for",
    "order",
    "you",
    "not",
    "have",
    "and",
    "with",
    "it",
    "can",
    "please",
    "how",
    "why",
    "what",
    "when",
    "where",
    "your",
    "this",
    "that",
    "from",
    "was",
    "are",
    "will",
    "help",
    "amazon",
    "package",
    "delivery",
    "refund",
    "account",
}


def has_non_latin_script(text):
    """
    Quickly detect scripts that are clearly not English/Latin.
    """

    non_latin_ranges = [
        (0x3040, 0x30FF),  # Japanese
        (0x4E00, 0x9FFF),  # Chinese
        (0xAC00, 0xD7AF),  # Korean
        (0x0600, 0x06FF),  # Arabic
        (0x0400, 0x04FF),  # Cyrillic
        (0x0900, 0x097F),  # Devanagari
        (0x0370, 0x03FF),  # Greek
    ]

    for char in text:
        code = ord(char)

        for start, end in non_latin_ranges:
            if start <= code <= end:
                return True

    return False


def english_score(text):
    """
    Estimate whether a Latin-script message is English.

    This is a lightweight heuristic, not a perfect language classifier.
    """

    text = text.lower()

    words = re.findall(
        r"[a-z]+",
        text
    )

    if not words:
        return 0

    matches = sum(
        word in ENGLISH_WORDS
        for word in words
    )

    return matches


def is_english(text):
    """
    Keep messages that have strong evidence of English.
    """

    text = str(text).strip()

    if len(text) < 10:
        return False

    # Remove obvious non-Latin languages first.
    if has_non_latin_script(text):
        return False

    words = re.findall(
        r"[a-z]+",
        text.lower()
    )

    if not words:
        return False

    score = english_score(text)

    # Strong signal:
    # at least two common English words.
    if score >= 2:
        return True

    # For longer messages, allow one English keyword if
    # the message contains enough Latin text.
    if len(words) >= 8 and score >= 1:
        return True

    return False


def clean_twitter_mentions(text):
    """
    Remove Twitter-style @mentions.
    """

    text = str(text)

    text = re.sub(
        r"(?<![\w@])@[A-Za-z0-9_]+",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def is_acknowledgement(text):
    """
    Remove obvious acknowledgement messages.
    """

    text = text.lower().strip()

    acknowledgement_patterns = [
        "thank you",
        "thanks",
        "thank u",
        "you're welcome",
        "youre welcome",
        "okay thanks",
        "ok thanks",
        "thanks again",
        "much appreciated",
    ]

    return any(
        text == pattern
        or text.startswith(pattern + " ")
        for pattern in acknowledgement_patterns
    )


def main():

    print("=" * 70)
    print("HIVER AI SUPPORT AGENT - PREPARE AMAZONHELP ENGLISH DATA")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        return

    print("\nReading dataset...")

    df = pd.read_csv(
        DATA_PATH,
        usecols=[
            "tweet_id",
            "author_id",
            "inbound",
            "created_at",
            "text",
            "in_response_to_tweet_id",
        ],
    )

    print(
        f"Total tweets: {len(df):,}"
    )

    # ---------------------------------------------------------
    # 1. Select AmazonHelp support tweets
    # ---------------------------------------------------------

    support = df[
        (df["author_id"] == BRAND)
        & (df["inbound"] == False)
    ].copy()

    print(
        f"AmazonHelp support tweets: "
        f"{len(support):,}"
    )

    # ---------------------------------------------------------
    # 2. Build tweet lookup
    # ---------------------------------------------------------

    tweet_lookup = df.set_index("tweet_id")

    pairs = []

    for _, support_tweet in support.iterrows():

        parent_id = support_tweet[
            "in_response_to_tweet_id"
        ]

        if pd.isna(parent_id):
            continue

        parent_id = int(parent_id)

        if parent_id not in tweet_lookup.index:
            continue

        parent = tweet_lookup.loc[parent_id]

        if not bool(parent["inbound"]):
            continue

        customer_text = str(
            parent["text"]
        ).strip()

        support_text = str(
            support_tweet["text"]
        ).strip()

        if not customer_text or not support_text:
            continue

        pairs.append(
            {
                "customer_tweet_id": parent_id,
                "support_tweet_id": int(
                    support_tweet["tweet_id"]
                ),
                "customer_text": customer_text,
                "support_text": support_text,
                "customer_created_at": parent[
                    "created_at"
                ],
                "support_created_at": support_tweet[
                    "created_at"
                ],
            }
        )

    pairs_df = pd.DataFrame(pairs)

    print(
        f"Direct customer -> AmazonHelp pairs: "
        f"{len(pairs_df):,}"
    )

    # ---------------------------------------------------------
    # 3. Remove empty messages
    # ---------------------------------------------------------

    pairs_df = pairs_df.dropna(
        subset=[
            "customer_text",
            "support_text",
        ]
    )

    pairs_df = pairs_df[
        (pairs_df["customer_text"].str.len() > 0)
        & (pairs_df["support_text"].str.len() > 0)
    ]

    # ---------------------------------------------------------
    # 4. Fast English filtering
    # ---------------------------------------------------------

    print(
        "\nApplying fast English-language filter..."
    )

    english_mask = pairs_df[
        "customer_text"
    ].apply(is_english)

    english_pairs = pairs_df[
        english_mask
    ].copy()

    print(
        f"English candidates: "
        f"{len(english_pairs):,}"
    )

    print(
        f"Removed as non-English/low-confidence: "
        f"{len(pairs_df) - len(english_pairs):,}"
    )

    # ---------------------------------------------------------
    # 5. Clean mentions
    # ---------------------------------------------------------

    english_pairs["customer_text"] = (
        english_pairs["customer_text"]
        .apply(clean_twitter_mentions)
    )

    english_pairs["support_text"] = (
        english_pairs["support_text"]
        .apply(clean_twitter_mentions)
    )

    # ---------------------------------------------------------
    # 6. Remove short messages
    # ---------------------------------------------------------

    english_pairs = english_pairs[
        english_pairs["customer_text"].str.len() >= 10
    ]

    print(
        f"After short-message removal: "
        f"{len(english_pairs):,}"
    )

    # ---------------------------------------------------------
    # 7. Remove acknowledgements
    # ---------------------------------------------------------

    english_pairs = english_pairs[
        ~english_pairs["customer_text"].apply(
            is_acknowledgement
        )
    ]

    print(
        f"After acknowledgement removal: "
        f"{len(english_pairs):,}"
    )

    # ---------------------------------------------------------
    # 8. Remove duplicate customer messages
    # ---------------------------------------------------------

    english_pairs = english_pairs.drop_duplicates(
        subset=["customer_text"]
    )

    print(
        f"After duplicate removal: "
        f"{len(english_pairs):,}"
    )

    # ---------------------------------------------------------
    # 9. Save JSONL
    # ---------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:

        for _, row in english_pairs.iterrows():

            record = {
                "customer_tweet_id": int(
                    row["customer_tweet_id"]
                ),
                "support_tweet_id": int(
                    row["support_tweet_id"]
                ),
                "customer_text": row[
                    "customer_text"
                ],
                "support_text": row[
                    "support_text"
                ],
                "customer_created_at": row[
                    "customer_created_at"
                ],
                "support_created_at": row[
                    "support_created_at"
                ],
            }

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )

    print("\nSaved:")
    print(OUTPUT_PATH)

    print(
        f"\nFinal cleaned English pairs: "
        f"{len(english_pairs):,}"
    )

    print("\nData preparation complete.")


if __name__ == "__main__":
    main()
    