from retriever import HistoricalRetriever


def main():

    retriever = HistoricalRetriever()

    query = "My package was supposed to arrive yesterday but I still haven't received it."

    results = retriever.search(query, top_k=3)

    print(f"\nQuery: {query}")

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Customer: {result['customer_text']}")
        print(f"AmazonHelp: {result['support_text']}")


if __name__ == "__main__":
    main()
    