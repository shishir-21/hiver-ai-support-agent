from llm_classifier import LLMIntentClassifier


def main():

    classifier = LLMIntentClassifier()

    test_messages = [
    "Someone hacked my Amazon account and changed my email.",
    "I don't recognize a charge on my Amazon account.",
    "My Prime delivery is two days late.",
    "I have Prime but my package still hasn't arrived.",
    "The package says delivered but I never received it.",
    "I received the wrong item in my order.",
    "I want my money back because the item arrived damaged.",
    "Alexa is not responding to my voice commands.",
    "I want to close my Amazon account.",
    "Thank you Amazon for helping me with my order!",
    "Amazon is great, I love Prime.",
    "My order is late and I want a refund.",
    ]

    for message in test_messages:

        result = classifier.predict(message)

        print("\nCustomer:")
        print(message)

        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"Reason: {result['reason']}")


if __name__ == "__main__":
    main()
    