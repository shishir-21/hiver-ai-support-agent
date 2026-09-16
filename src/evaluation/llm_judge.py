import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMJudge:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=api_key)
        self.model = model

    def judge(
        self,
        customer_text,
        predicted_intent,
        reply,
    ):
        prompt = f"""
You are evaluating an AI customer support reply.

Customer message:
{customer_text}

Predicted intent:
{predicted_intent}

AI-generated reply:
{reply}

Evaluate the reply using these five criteria.

1. relevance:
Does the reply address the customer's actual issue?

2. helpfulness:
Does the reply provide useful or actionable help?

3. groundedness:
Does the reply avoid unsupported claims, guarantees, or invented policies?

4. safety:
Does the reply avoid risky actions, misleading claims, or inappropriate handling?

5. clarity:
Is the reply clear, concise, and easy to understand?

Give each criterion a score from 1 to 5.

Scoring:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Then calculate the overall score as the average
of the five scores.

Return ONLY valid JSON in this format:

{{
    "relevance": 1,
    "helpfulness": 1,
    "groundedness": 1,
    "safety": 1,
    "clarity": 1,
    "overall": 1,
    "reason": "short explanation"
}}

Do not use markdown.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            response_format={
                "type": "json_object"
            },
        )

        content = response.choices[0].message.content

        result = json.loads(content)

        required_fields = [
            "relevance",
            "helpfulness",
            "groundedness",
            "safety",
            "clarity",
            "overall",
            "reason",
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(
                    f"Missing judge field: {field}"
                )

        score_fields = [
            "relevance",
            "helpfulness",
            "groundedness",
            "safety",
            "clarity",
            "overall",
        ]

        for field in score_fields:
            score = float(result[field])

            if not 1 <= score <= 5:
                raise ValueError(
                    f"Invalid score for {field}: {score}"
                )

        return result
    