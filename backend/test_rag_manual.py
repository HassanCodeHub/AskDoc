from app.rag import ask_document


question = "What are the project expenses?"

result = ask_document(
    question,
    top_k=3
)

print("\n========== RAG ANSWER ==========\n")

print(result["answer"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print(
        f"Chunk: {source['chunk_id']} | "
        f"Page: {source['page_number']} | "
        f"Similarity: {source['similarity']:.4f}"
    )