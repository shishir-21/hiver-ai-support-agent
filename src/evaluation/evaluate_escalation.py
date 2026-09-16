import pandas as pd

from src.escalation.policy import EscalationPolicy


GOLDEN_FILE = "data/golden/amazon_golden_200_annotated.csv"


def main():

    df = pd.read_csv(
        GOLDEN_FILE,
        dtype=str,
    ).fillna("")

    policy = EscalationPolicy()

    results = []

    for _, row in df.iterrows():

        customer_text = row["customer_text"]
        human_label = row["escalation"]

        decision = policy.decide(
            customer_text,
            row["intent"],
        )

        predicted_label = decision["escalation"]
        reason = decision["reason"]

        results.append({
            "customer_tweet_id": row["customer_tweet_id"],
            "customer_text": customer_text,
            "human_escalation": human_label,
            "predicted_escalation": predicted_label,
            "reason": reason,
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        "data/golden/escalation_predictions.csv",
        index=False,
    )

    # Confusion matrix counts.
    true_auto_pred_auto = (
        (results_df["human_escalation"] == "auto_handle")
        & (results_df["predicted_escalation"] == "auto_handle")
    ).sum()

    true_auto_pred_escalate = (
        (results_df["human_escalation"] == "auto_handle")
        & (results_df["predicted_escalation"] == "escalate")
    ).sum()

    true_escalate_pred_auto = (
        (results_df["human_escalation"] == "escalate")
        & (results_df["predicted_escalation"] == "auto_handle")
    ).sum()

    true_escalate_pred_escalate = (
        (results_df["human_escalation"] == "escalate")
        & (results_df["predicted_escalation"] == "escalate")
    ).sum()

    total = len(results_df)

    accuracy = (
        true_auto_pred_auto
        + true_escalate_pred_escalate
    ) / total

    # For the "escalate" class:
    precision = (
        true_escalate_pred_escalate
        / (
            true_escalate_pred_escalate
            + true_auto_pred_escalate
        )
        if (
            true_escalate_pred_escalate
            + true_auto_pred_escalate
        )
        else 0
    )

    recall = (
        true_escalate_pred_escalate
        / (
            true_escalate_pred_escalate
            + true_escalate_pred_auto
        )
        if (
            true_escalate_pred_escalate
            + true_escalate_pred_auto
        )
        else 0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall
        else 0
    )

    # Unsafe auto-handle:
    # human says escalate, but policy says auto_handle.
    unsafe_auto_handle_rate = (
        true_escalate_pred_auto
        / (
            true_escalate_pred_auto
            + true_escalate_pred_escalate
        )
        if (
            true_escalate_pred_auto
            + true_escalate_pred_escalate
        )
        else 0
    )

    print("\nEscalation Evaluation")
    print("=====================")

    print(f"Total examples: {total}")

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")

    print(
        "\nUnsafe auto-handle rate: "
        f"{unsafe_auto_handle_rate:.4f}"
    )

    print("\nConfusion Matrix")
    print("----------------")
    print(
        "                     Predicted"
    )
    print(
        "                 auto_handle  escalate"
    )
    print(
        f"Human auto_handle "
        f"{true_auto_pred_auto:12} "
        f"{true_auto_pred_escalate:9}"
    )
    print(
        f"Human escalate    "
        f"{true_escalate_pred_auto:12} "
        f"{true_escalate_pred_escalate:9}"
    )

    print(
        "\nPredictions saved to:"
        " data/golden/escalation_predictions.csv"
    )


if __name__ == "__main__":
    main()
    