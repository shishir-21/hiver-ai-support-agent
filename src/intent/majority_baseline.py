import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold


INPUT_FILE = "data/golden/amazon_golden_200_annotated.csv"

RANDOM_SEED = 42
N_SPLITS = 5


def main():
    df = pd.read_csv(INPUT_FILE)

    X = df["customer_text"]
    y = df["intent"]

    skf = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED,
    )

    all_true = []
    all_predictions = []
    majority_intents = []

    for fold, (train_index, test_index) in enumerate(
        skf.split(X, y),
        start=1,
    ):
        train_y = y.iloc[train_index]
        test_y = y.iloc[test_index]

        # Find majority intent only from the training fold.
        majority_intent = train_y.value_counts().idxmax()

        predictions = [majority_intent] * len(test_y)

        all_true.extend(test_y.tolist())
        all_predictions.extend(predictions)
        majority_intents.append(majority_intent)

        fold_accuracy = accuracy_score(test_y, predictions)
        fold_macro_f1 = f1_score(
            test_y,
            predictions,
            average="macro",
            zero_division=0,
        )

        print(
            f"Fold {fold}: "
            f"majority={majority_intent}, "
            f"accuracy={fold_accuracy:.4f}, "
            f"macro_f1={fold_macro_f1:.4f}"
        )

    accuracy = accuracy_score(
        all_true,
        all_predictions,
    )

    macro_f1 = f1_score(
        all_true,
        all_predictions,
        average="macro",
        zero_division=0,
    )

    print("\n" + "=" * 70)
    print("MAJORITY-CLASS BASELINE")
    print("=" * 70)

    print(f"\nTotal examples: {len(df)}")
    print(f"Cross-validation folds: {N_SPLITS}")

    print("\nMajority intents by fold:")
    for i, intent in enumerate(majority_intents, start=1):
        print(f"Fold {i}: {intent}")

    print(f"\nOverall Accuracy: {accuracy:.4f}")
    print(f"Overall Macro-F1: {macro_f1:.4f}")


if __name__ == "__main__":
    main()
    