from app.retrieval import retrieve_chunks


query = "What are the project expenses?"

results = retrieve_chunks(
    query=query,
    top_k=3
)

print("\n========== RETRIEVAL RESULTS ==========\n")

for index, result in enumerate(results, start=1):

    print(f"Result #{index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Document ID: {result['document_id']}")
    print(f"Page: {result['page_number']}")
    print(f"Similarity: {result['similarity']:.4f}")
    print(f"Text: {result['chunk_text'][:300]}")
    print("-" * 60)