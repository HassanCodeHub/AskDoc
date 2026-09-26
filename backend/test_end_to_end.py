from app.rag import ask_document


questions = [
    "What is the total amount collected?",
    "What components are used in the IoT Based Health Monitoring System?",
    "What is the population of Japan?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    result = ask_document(
        question,
        top_k=3
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"Chunk ID: {source['chunk_id']} | "
            f"Page: {source['page_number']} | "
            f"Similarity: {source['similarity']:.4f}"
        )