from app.rag import build_rag_prompt


def test_rag_prompt_contains_question():
    question = "What were the project expenses?"

    chunks = [
        {
            "page_number": 1,
            "chunk_text": "PROJECT EXPENSES: Total amount collected = 3,100"
        }
    ]

    prompt = build_rag_prompt(
        question,
        chunks
    )

    assert question in prompt


def test_rag_prompt_contains_page_number():
    chunks = [
        {
            "page_number": 3,
            "chunk_text": "Some document information."
        }
    ]

    prompt = build_rag_prompt(
        "What is this about?",
        chunks
    )

    assert "[Page 3]" in prompt


def test_rag_prompt_forbids_outside_knowledge():
    prompt = build_rag_prompt(
        "Test question",
        []
    )

    assert "Do not use outside knowledge." in prompt