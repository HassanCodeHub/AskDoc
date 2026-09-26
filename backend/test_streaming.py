from app.rag import build_rag_prompt, stream_groq_answer


question = "What is the total amount collected?"

retrieved_chunks = [
    {
        "page_number": 1,
        "chunk_text": (
            "PROJECT EXPENSES "
            "(Total Amount Collected = 3,100)"
        )
    }
]

prompt = build_rag_prompt(
    question,
    retrieved_chunks
)

print("\n========== STREAMING TEST ==========\n")

for text in stream_groq_answer(prompt):
    print(text, end="", flush=True)

print("\n\n========== STREAMING COMPLETE ==========\n")