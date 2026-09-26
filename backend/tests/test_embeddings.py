from app.embeddings import generate_embedding


def test_generate_embedding():
    text = "This is a test document about project expenses."

    embedding = generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384


def test_generate_embedding_rejects_empty_text():
    try:
        generate_embedding("")
        assert False
    except ValueError:
        assert True