from sentence_transformers import SentenceTransformer


# Load the model once when this module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Generate a 384-dimensional embedding for the given text.

    Returns:
        list: Embedding vector as a normal Python list.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = model.encode(text)

    return embedding.tolist()