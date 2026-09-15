import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMIntentClassifier:

    INTENTS = {
        "delivery_issue": (
            "Delivery or tracking problems, including delayed, lost, "
            "not shipped, or delivered-but-not-received packages."
        ),

        "order_or_product_issue": (
            "Wrong, damaged, or missing product contents after receiving "
            "the order. Do not use for a package that has not arrived."
        ),

        "return_or_refund": (
            "Explicit requests for a return, refund, or money back."
        ),

        "payment_or_amazon_pay": (
            "Payment failures, unexpected charges, payment transactions, "
            "Amazon Pay, or suspicious financial activity."
        ),

        "account_access_or_security": (
            "Login problems, locked accounts, hacked accounts, password "
            "or email changes, account closure, or account security."
        ),

        "prime_membership_or_benefit": (
            "Prime membership, renewal, cancellation, accidental signup, "
            "or complaints about Prime benefits."
        ),

        "product_or_technical_issue": (
            "Amazon devices, apps, websites, Alexa, Echo, Fire TV, Kindle, "
            "Amazon Music, or other technical/product functionality problems."
        ),

        "feedback_or_praise": (
            "Praise, appreciation, or general feedback without a concrete "
            "support problem or request."
        ),
    }

    PRIORITY_RULES = """
If multiple intents appear, use these priority rules:

1. Account security/access
2. Payment or financial transaction
3. Explicit return/refund request
4. Wrong/damaged/missing product after receiving the order
5. Delivery/tracking/missing package
6. Product/device/app/website technical problem
7. Prime membership/benefit as the main issue
8. Feedback or praise when there is no concrete support problem

Important:
- A security issue stays account_access_or_security even if an order
  or payment is also mentioned.
- A payment issue stays payment_or_amazon_pay when the financial
  transaction is the main problem.
- A missing package is delivery_issue, not order_or_product_issue.
- Prime should be selected only when Prime membership/benefits are
  the main issue. If Prime is only background and the actual problem
  is delivery, use delivery_issue.
- Concrete problems with emotion are NOT feedback_or_praise.
"""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")

        if not model:
            raise ValueError("GROQ_MODEL is missing from .env")

        self.client = Groq(api_key=api_key)
        self.model = model

    def predict(self, customer_text):

        intent_list = "\n".join(
            f"- {name}: {description}"
            for name, description in self.INTENTS.items()
        )

        prompt = f"""
You are an Amazon customer-support intent classifier.

Classify the customer's message into exactly ONE of the allowed intents.

Allowed intents:

{intent_list}

{self.PRIORITY_RULES}

Customer message:
{customer_text}

Return ONLY valid JSON in exactly this format:

{{
  "intent": "one_allowed_intent",
  "confidence": 0.0,
  "reason": "short explanation"
}}

Rules:
- The intent MUST be one of the allowed intents.
- Confidence must be a number between 0 and 1.
- Do not add any other JSON fields.
- Do not use markdown.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You classify customer-support messages accurately and return strict JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        result = json.loads(content)

        if result["intent"] not in self.INTENTS:
            raise ValueError(
                f"Invalid intent returned by model: {result['intent']}"
            )

        result["confidence"] = float(result["confidence"])

        return result
    