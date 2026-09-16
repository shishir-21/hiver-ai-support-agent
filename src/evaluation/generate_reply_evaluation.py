import os
import pandas as pd

from src.retrieval.retriever import HistoricalRetriever
from src.generation.reply_generator import ReplyGenerator


GOLDEN_FILE = "data/golden/amazon_golden_200_annotated.csv"
PREDICTIONS_FILE = "data/golden/llm_intent_predictions.csv"
OUTPUT_FILE = "data/golden/reply_evaluation.csv"


def main():
    golden_df = pd.read_csv(
        GOLDEN_FILE,
        dtype=str,
    ).fillna("")

    predictions_df = pd.read_csv(
        PREDICTIONS_FILE,
        dtype=str,
    ).fillna("")

    if os.path.exists(OUTPUT_FILE):
        results_df = pd.read_csv(
            OUTPUT_FILE,
            dtype=str,
        ).fillna("")

        completed_ids = set(
            results_df["customer_tweet_id"]
        )

        results = results_df.to_dict("records")

        print(
            f"Resuming from existing file. "
            f"Already completed: {len(results)}"
        )

    else:
        completed_ids = set()
        results = []

    retriever = HistoricalRetriever()
    generator = ReplyGenerator()

    for index, row in golden_df.iterrows():

        customer_id = row["customer_tweet_id"]

        if customer_id in completed_ids:
            continue

        customer_text = row["customer_text"]

        prediction = predictions_df[
            predictions_df["customer_tweet_id"] == customer_id
        ]

        if prediction.empty:
            print(
                f"Skipping {index + 1}: "
                "prediction not found"
            )
            continue

        predicted_intent = prediction.iloc[0]["predicted_intent"]

        examples = retriever.search(
            customer_text,
            top_k=3,
        )

        try:
            reply = generator.generate(
                customer_text=customer_text,
                intent=predicted_intent,
                retrieved_examples=examples,
            )

        except Exception as error:
            print(
                f"\nStopped at example {index + 1}."
            )
            print(f"Error: {error}")
            break

        results.append({
            "customer_tweet_id": customer_id,
            "customer_text": customer_text,
            "gold_intent": row["intent"],
            "predicted_intent": predicted_intent,
            "reply": reply,
        })

        completed_ids.add(customer_id)

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False,
        )

        print(
            f"[{index + 1}/{len(golden_df)}] "
            f"Saved reply"
        )

    print("\nCurrent replies saved:")
    print(len(results))
    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    