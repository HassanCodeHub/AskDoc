import json

from app.db import get_db_connection
from app.embeddings import generate_embedding


def generate_embeddings_for_chunks():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Get chunks that don't have embeddings yet
            cursor.execute("""
                SELECT id, chunk_text
                FROM chunks
                WHERE embedding IS NULL
            """)

            chunks = cursor.fetchall()

            print(f"Found {len(chunks)} chunks without embeddings.")

            for chunk in chunks:

                print(f"Generating embedding for chunk {chunk['id']}...")

                embedding = generate_embedding(
                    chunk["chunk_text"]
                )

                embedding_json = json.dumps(embedding)

                cursor.execute("""
                    UPDATE chunks
                    SET embedding = %s
                    WHERE id = %s
                """, (
                    embedding_json,
                    chunk["id"]
                ))

            connection.commit()

            print("Embedding generation completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    generate_embeddings_for_chunks()