import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/golden/amazon_golden_200.csv")
OUTPUT_FILE = Path("data/golden/amazon_golden_200_annotated.csv")

INTENTS = [
    "delivery_issue",
    "order_or_product_issue",
    "return_or_refund",
    "payment_or_amazon_pay",
    "account_access_or_security",
    "prime_membership_or_benefit",
    "product_or_technical_issue",
    "feedback_or_praise",
]

ESCALATION_OPTIONS = [
    "auto_handle",
    "escalate",
]

ANNOTATOR = "human"


def show_intents():
    print("\nINTENTS:")
    for i, intent in enumerate(INTENTS, start=1):
        print(f"{i}. {intent}")


def show_escalation_options():
    print("\nESCALATION:")
    print("1. auto_handle")
    print("2. escalate")


def main():
    df = pd.read_csv(INPUT_FILE, dtype=str).fillna("")

    # Resume from an existing annotation file if available.
    if OUTPUT_FILE.exists():
        df = pd.read_csv(OUTPUT_FILE, dtype=str).fillna("")
        print(f"Resuming from: {OUTPUT_FILE}")

    for index, row in df.iterrows():

        # Skip already annotated rows.
        if (
            pd.notna(row.get("intent"))
            and str(row.get("intent")).strip() != ""
        ):
            continue

        print("\n" + "=" * 80)
        print(f"EXAMPLE {index + 1} / {len(df)}")
        print("=" * 80)

        print(f"\nCustomer tweet ID: {row['customer_tweet_id']}")
        print(f"\nCustomer:\n{row['customer_text']}")
        print(f"\nHistorical support reply:\n{row['support_text']}")

        show_intents()

        while True:
            try:
                choice = int(input("\nChoose intent number: "))
                if 1 <= choice <= len(INTENTS):
                    intent = INTENTS[choice - 1]
                    break
            except ValueError:
                pass

            print("Invalid choice. Please enter a valid intent number.")

        show_escalation_options()

        while True:
            try:
                choice = int(input("\nChoose escalation (1 or 2): "))
                if choice in [1, 2]:
                    escalation = ESCALATION_OPTIONS[choice - 1]
                    break
            except ValueError:
                pass

            print("Invalid choice. Enter 1 or 2.")

        escalation_reason = input(
            "\nEscalation reason "
            "(write 'none' for auto_handle): "
        ).strip()

        if not escalation_reason:
            escalation_reason = "none"

        df.at[index, "intent"] = intent
        df.at[index, "escalation"] = escalation
        df.at[index, "escalation_reason"] = escalation_reason
        df.at[index, "annotator"] = ANNOTATOR

        # Save after every example so progress is not lost.
        df.to_csv(OUTPUT_FILE, index=False)

        print("\nSaved.")

    print("\n" + "=" * 80)
    print("ANNOTATION COMPLETE")
    print("=" * 80)
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    