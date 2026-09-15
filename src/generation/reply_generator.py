import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


MODEL_NAME = os.getenv("GROQ_MODEL")


class ReplyGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=api_key)

    def generate(self, customer_text, intent, retrieved_examples):
        examples_text = ""

        for i, example in enumerate(retrieved_examples, start=1):
            examples_text += (
                f"\nExample {i}:\n"
                f"Customer: {example['customer_text']}\n"
                f"Support: {example['support_text']}\n"
            )

        prompt = f"""
You are a customer support assistant for AmazonHelp.

Customer message:
{customer_text}

Detected intent:
{intent}

Here are similar historical customer-support conversations:
{examples_text}

Write a short, helpful support reply.

Rules:
- Use the historical examples as guidance.
- Do not invent policies, refunds, guarantees, or facts.
- Do not claim that an action has already been completed.
- Do not expose internal reasoning.
- Do not mention these historical examples.
- Do not copy a historical response word-for-word.
- Never include URLs or links in the reply.
- If a historical example contains a URL, use the information from it
  as guidance but do not copy the URL.
- If more information is needed, politely ask the customer for it.
- Keep the response concise and natural.
"""

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You write concise and safe customer support replies.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
    