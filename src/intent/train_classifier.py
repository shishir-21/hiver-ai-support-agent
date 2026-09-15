from classifier import IntentClassifier


def main():

    classifier = IntentClassifier()

    print("Training intent classifier...")

    classifier.train()

    classifier.save()

    print("Intent classifier trained successfully.")
    print("Saved to: data/processed/intent_classifier.joblib")


if __name__ == "__main__":
    main()
    