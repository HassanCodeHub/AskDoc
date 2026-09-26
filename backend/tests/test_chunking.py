from app.chunking import chunk_page_text


def test_chunk_page_text():
    text = " ".join(f"word{i}" for i in range(1, 951))

    chunks = chunk_page_text(
        text,
        page_number=3,
        chunk_size=500,
        overlap=50
    )

    assert len(chunks) == 2

    # Both chunks belong to page 3
    assert chunks[0]["page_number"] == 3
    assert chunks[1]["page_number"] == 3

    first_words = chunks[0]["chunk_text"].split()
    second_words = chunks[1]["chunk_text"].split()

    assert len(first_words) == 500
    assert len(second_words) == 500

    # Verify 50-word overlap
    assert first_words[-50:] == second_words[:50]


def test_empty_page():
    chunks = chunk_page_text(
        "",
        page_number=1
    )

    assert chunks == []


def test_invalid_overlap():
    text = "hello world"

    try:
        chunk_page_text(
            text,
            page_number=1,
            chunk_size=100,
            overlap=100
        )
        assert False
    except ValueError:
        assert True