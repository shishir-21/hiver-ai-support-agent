from src.intent.llm_classifier import LLMIntentClassifier
from src.retrieval.retriever import HistoricalRetriever
from src.generation.reply_generator import ReplyGenerator


customer_text = (
    "My package was supposed to arrive yesterday "
    "but I still haven't received it."
)

classifier = LLMIntentClassifier()
retriever = HistoricalRetriever()
generator = ReplyGenerator()

classification = classifier.predict(customer_text)

examples = retriever.search(
    customer_text,
    top_k=3
)

reply = generator.generate(
    customer_text=customer_text,
    intent=classification["intent"],
    retrieved_examples=examples,
)

print("\nIntent:")
print(classification["intent"])

print("\nGenerated Reply:")
print(reply)
