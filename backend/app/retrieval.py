import json

import numpy as np

from .db import get_db_connection
from .embeddings import generate_embedding


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    vector_a = np.array(vector_a, dtype=float)
    vector_b = np.array(vector_b, dtype=float)

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b) / (norm_a * norm_b)
    )


def retrieve_chunks(query, top_k=3, document_id=None):
    """
    Retrieve the most relevant document chunks for a query.

    If document_id is provided, retrieval is restricted
    to that specific document.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    # Generate embedding for the user's question
    query_embedding = generate_embedding(query)

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            if document_id is not None:
                cursor.execute("""
                    SELECT
                        id,
                        document_id,
                        chunk_text,
                        page_number,
                        embedding
                    FROM chunks
                    WHERE embedding IS NOT NULL
                    AND document_id = %s
                """, (document_id,))

            else:
                cursor.execute("""
                    SELECT
                        id,
                        document_id,
                        chunk_text,
                        page_number,
                        embedding
                    FROM chunks
                    WHERE embedding IS NOT NULL
                """)

            chunks = cursor.fetchall()

    finally:
        connection.close()

    results = []

    for chunk in chunks:

        stored_embedding = json.loads(
            chunk["embedding"]
        )

        similarity = cosine_similarity(
            query_embedding,
            stored_embedding
        )

        results.append({
            "chunk_id": chunk["id"],
            "document_id": chunk["document_id"],
            "page_number": chunk["page_number"],
            "chunk_text": chunk["chunk_text"],
            "similarity": similarity
        })

    # Highest similarity first
    results.sort(
        key=lambda result: result["similarity"],
        reverse=True
    )

    return results[:top_k]