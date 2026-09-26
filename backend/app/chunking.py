def chunk_page_text(text, page_number, chunk_size=500, overlap=50):
    """
    Split text from a single PDF page into overlapping chunks.

    Each returned chunk keeps the page number it came from.
    """

    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(words):

        remaining_words = len(words) - start

        # Don't create a tiny chunk that is mostly duplicated
        # from the previous chunk.
        if chunks and remaining_words <= overlap:
            break

        end = min(start + chunk_size, len(words))

        chunk_words = words[start:end]

        chunks.append({
            "page_number": page_number,
            "chunk_text": " ".join(chunk_words)
        })

        start += step

    return chunks