from src.agent import SupportAgent


agent = SupportAgent()


test_cases = [
    "Where is my package?",
    "My package is two days late.",
    "Someone hacked my Amazon account and changed my email address.",
    "I don't recognize this charge on my account.",
    "My order says delivered but I did not receive it.",
    "I want to return this damaged item and get my money back.",
    "How can I cancel my Prime membership?",
    "My Fire TV is not working.",
    "Amazon has been really helpful, thank you!",
]


for customer_text in test_cases:

    result = agent.analyze(customer_text)

    print("\n" + "=" * 70)

    print("\nCustomer:")
    print(result["customer_text"])

    print("\nIntent:")
    print(result["intent"])

    print("\nConfidence:")
    print(result["intent_confidence"])

    print("\nGenerated Reply:")
    print(result["reply"])

    print("\nEscalation:")
    print(result["escalation"])

    print("\nEscalation Reason:")
    print(result["escalation_reason"])
    