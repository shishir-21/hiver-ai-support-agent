import pandas as pd

from sklearn.metrics import accuracy_score, f1_score, classification_report
from src.intent.llm_classifier import LLMIntentClassifier


GOLDEN_FILE = "data/golden/amazon_golden_200_annotated.csv"
OUTPUT_FILE = "data/golden/llm_intent_predictions.csv"


def main():
    df = pd.read_csv(GOLDEN_FILE, dtype=str).fillna("")

    classifier = LLMIntentClassifier()

    predictions = []

    for index, row in df.iterrows():
        text = row["customer_text"]
        true_intent = row["intent"]

        result = classifier.predict(text)

        predictions.append({
            "customer_tweet_id": row["customer_tweet_id"],
            "customer_text": text,
            "true_intent": true_intent,
            "predicted_intent": result["intent"],
            "confidence": result["confidence"],
            "reason": result["reason"],
        })

        print(
            f"[{index + 1}/{len(df)}] "
            f"True: {true_intent} | "
            f"Predicted: {result['intent']}"
        )

    predictions_df = pd.DataFrame(predictions)

    y_true = predictions_df["true_intent"]
    y_pred = predictions_df["predicted_intent"]

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    print("\n" + "=" * 60)
    print("LLM INTENT EVALUATION")
    print("=" * 60)

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Macro-F1: {macro_f1:.4f}")

    print("\nPer-intent results:")
    print(
        classification_report(
            y_true,
            y_pred,
            zero_division=0,
        )
    )

    predictions_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(f"Predictions saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    