from app.retrieval import cosine_similarity


def test_cosine_similarity_identical_vectors():
    vector_a = [1, 0, 0]
    vector_b = [1, 0, 0]

    similarity = cosine_similarity(
        vector_a,
        vector_b
    )

    assert similarity == 1.0


def test_cosine_similarity_orthogonal_vectors():
    vector_a = [1, 0, 0]
    vector_b = [0, 1, 0]

    similarity = cosine_similarity(
        vector_a,
        vector_b
    )

    assert similarity == 0.0


def test_cosine_similarity_zero_vector():
    vector_a = [0, 0, 0]
    vector_b = [1, 0, 0]

    similarity = cosine_similarity(
        vector_a,
        vector_b
    )

    assert similarity == 0.0