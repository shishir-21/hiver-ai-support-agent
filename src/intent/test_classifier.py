from classifier import IntentClassifier


def main():

    classifier = IntentClassifier()
    classifier.load()

    test_messages = [
        "My package has not arrived yet.",
        "I was charged for something I didn't buy.",
        "I cannot log into my Amazon account.",
        "I want to cancel my Prime membership.",
        "I want a refund for this order.",
        "The item I received is damaged.",
        "My Fire TV is not working.",
        "Thanks Amazon, your support was really helpful!",
    ]

    for message in test_messages:

        intent, confidence = classifier.predict(message)

        print("\nCustomer:")
        print(message)

        print(f"Intent: {intent}")
        print(f"Confidence: {confidence:.4f}")


if __name__ == "__main__":
    main()
    