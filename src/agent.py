from src.intent.llm_classifier import LLMIntentClassifier
from src.retrieval.retriever import HistoricalRetriever
from src.generation.reply_generator import ReplyGenerator
from src.escalation.policy import EscalationPolicy


class SupportAgent:
    def __init__(self):
        self.classifier = LLMIntentClassifier()
        self.retriever = HistoricalRetriever()
        self.reply_generator = ReplyGenerator()
        self.escalation_policy = EscalationPolicy()

    def analyze(self, customer_text, top_k=3):
        # 1. Classify the customer message
        classification = self.classifier.predict(customer_text)

        # 2. Retrieve similar historical conversations
        retrieved_examples = self.retriever.search(
            customer_text,
            top_k=top_k
        )

        # 3. Generate a grounded reply
        reply = self.reply_generator.generate(
            customer_text=customer_text,
            intent=classification["intent"],
            retrieved_examples=retrieved_examples,
        )

        # 4. Decide auto-handle or escalate
        escalation = self.escalation_policy.decide(
            customer_text=customer_text,
            intent=classification["intent"],
            retrieved_examples=retrieved_examples,
        )

        return {
            "customer_text": customer_text,
            "intent": classification["intent"],
            "intent_confidence": classification["confidence"],
            "intent_reason": classification["reason"],
            "retrieved_examples": retrieved_examples,
            "reply": reply,
            "escalation": escalation["escalation"],
            "escalation_reason": escalation["reason"],
        }
        