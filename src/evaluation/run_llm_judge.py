import os
import pandas as pd

from src.evaluation.llm_judge import LLMJudge


INPUT_FILE = "data/golden/reply_evaluation.csv"
OUTPUT_FILE = "data/golden/llm_reply_judgments.csv"


def main():

    input_df = pd.read_csv(
        INPUT_FILE,
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
            f"Already judged: {len(results)}"
        )

    else:

        completed_ids = set()
        results = []

    judge = LLMJudge()

    for index, row in input_df.iterrows():

        customer_id = row["customer_tweet_id"]

        if customer_id in completed_ids:
            continue

        print(
            f"\nJudging [{index + 1}/{len(input_df)}]"
        )

        try:

            result = judge.judge(
                customer_text=row["customer_text"],
                predicted_intent=row["predicted_intent"],
                reply=row["reply"],
            )

        except Exception as error:

            print(
                f"\nStopped at example {index + 1}."
            )
            print(f"Error: {error}")
            break

        results.append({
            "customer_tweet_id": customer_id,
            "customer_text": row["customer_text"],
            "predicted_intent": row["predicted_intent"],
            "reply": row["reply"],
            "relevance": result["relevance"],
            "helpfulness": result["helpfulness"],
            "groundedness": result["groundedness"],
            "safety": result["safety"],
            "clarity": result["clarity"],
            "overall": result["overall"],
            "reason": result["reason"],
        })

        completed_ids.add(customer_id)

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False,
        )

        print(
            f"Saved judgment "
            f"({len(results)}/{len(input_df)})"
        )

    print("\nCurrent judgments saved:")
    print(len(results))

    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    