import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold


INPUT_FILE = "data/golden/amazon_golden_200_annotated.csv"

RANDOM_SEED = 42
N_SPLITS = 5


def main():
    df = pd.read_csv(INPUT_FILE)

    X = df["customer_text"].fillna("")
    y = df["intent"]

    skf = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED,
    )

    all_true = []
    all_predictions = []

    for fold, (train_index, test_index) in enumerate(
        skf.split(X, y),
        start=1,
    ):
        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y.iloc[train_index]
        y_test = y.iloc[test_index]

        # Fit TF-IDF only on the training fold.
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_features=10000,
            sublinear_tf=True,
        )

        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        # Train a simple linear classifier.
        model = LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_SEED,
        )

        model.fit(X_train_tfidf, y_train)

        predictions = model.predict(X_test_tfidf)

        all_true.extend(y_test.tolist())
        all_predictions.extend(predictions)

        fold_accuracy = accuracy_score(
            y_test,
            predictions,
        )

        fold_macro_f1 = f1_score(
            y_test,
            predictions,
            average="macro",
            zero_division=0,
        )

        print(
            f"Fold {fold}: "
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
    print("TF-IDF + LOGISTIC REGRESSION BASELINE")
    print("=" * 70)

    print(f"\nTotal examples: {len(df)}")
    print(f"Cross-validation folds: {N_SPLITS}")

    print(f"\nOverall Accuracy: {accuracy:.4f}")
    print(f"Overall Macro-F1: {macro_f1:.4f}")


if __name__ == "__main__":
    main()
    