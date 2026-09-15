from src.escalation.policy import EscalationPolicy


policy = EscalationPolicy()


test_cases = [
    "Where is my package?",
    "My package is two days late.",
    "Someone hacked my Amazon account.",
    "I don't recognize this charge.",
    "My order says delivered but I did not receive it.",
    "I have already contacted you three times and still have no update.",
    "How can I cancel my Prime membership?",
]


for text in test_cases:
    result = policy.decide(
        customer_text=text,
        intent="delivery_issue",
    )

    print("\nCustomer:", text)
    print("Decision:", result["escalation"])
    print("Reason:", result["reason"])
    