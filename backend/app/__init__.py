import os
import json

import fitz
from .rag import (
    ask_document,
    prepare_streaming_rag,
    stream_groq_answer
)
from flask import Flask, request
from werkzeug.utils import secure_filename

from .db import get_db_connection
from .chunking import chunk_page_text
from .embeddings import generate_embedding


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "uploads"
)


def create_app():
    app = Flask(__name__)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @app.route("/api/questions/ask", methods=["POST"])
    def ask_question():

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        question = data.get("question")
        document_id = data.get("document_id")

        if not question:
            return {
                "message": "Question is required"
            }, 400

        if document_id is None:
            return {
                "message": "document_id is required"
            }, 400

        try:
            document_id = int(document_id)
        except (TypeError, ValueError):
            return {
                "message": "document_id must be an integer"
            }, 400

        try:

            result = ask_document(
                question=question,
                document_id=document_id
            )

            return result, 200

        except Exception as error:

            return {
                "message": "Failed to answer question",
                "error": str(error)
            }, 500

    @app.route("/api/questions/ask/stream", methods=["POST"])
    def ask_question_stream():

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        question = data.get("question")
        document_id = data.get("document_id")

        if not question:
            return {
                "message": "Question is required"
            }, 400

        if document_id is None:
            return {
                "message": "document_id is required"
            }, 400

        try:
            document_id = int(document_id)
        except (TypeError, ValueError):
            return {
                "message": "document_id must be an integer"
            }, 400

        try:
            prompt, retrieved_chunks = prepare_streaming_rag(
                question=question,
                document_id=document_id
            )

            if not retrieved_chunks:
                return {
                    "answer": "I couldn't find relevant information in the uploaded document.",
                    "sources": []
                }, 200

        except Exception as error:
            return {
                "message": "Failed to prepare question",
                "error": str(error)
            }, 500

        def generate():

            full_answer = ""

            try:

                for text in stream_groq_answer(prompt):

                    full_answer += text

                    yield json.dumps({
                        "type": "text",
                        "content": text
                    }) + "\n"

                import re

                # Normalize Unicode whitespace
                normalized_answer = full_answer.replace("\u202f", " ")

                # Find both:
                # [Page 1]
                # [Page 2]
                # [Page 3]
                cited_pages = set(
                    int(page)
                    for page in re.findall(
                        r"\[Page\s+(\d+)\]",
                        normalized_answer,
                        flags=re.IGNORECASE
                    )
                )

                sources = [
                    {
                        "chunk_id": chunk["chunk_id"],
                        "document_id": chunk["document_id"],
                        "page_number": chunk["page_number"],
                        "similarity": chunk["similarity"]
                    }
                    for chunk in retrieved_chunks
                    if chunk["page_number"] in cited_pages
                ]

                yield json.dumps({
                    "type": "sources",
                    "sources": sources
                }) + "\n"

                yield json.dumps({
                    "type": "done"
                }) + "\n"

            except Exception as error:

                yield json.dumps({
                    "type": "error",
                    "message": str(error)
                }) + "\n"

        response = app.response_class(
            generate(),
            mimetype="application/x-ndjson"
        )

        response.headers["Cache-Control"] = "no-cache"

        return response

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

        return response

    @app.route("/")
    def home():
        return {
            "message": "Smart Document Q&A API is running"
        }

    @app.route("/api/db-test")
    def db_test():
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT DATABASE() AS database_name"
                )

                result = cursor.fetchone()

            return {
                "status": "success",
                "database": result["database_name"]
            }

        finally:
            connection.close()

    @app.route("/api/documents/upload", methods=["POST"])
    def upload_document():

        # Check whether a file was provided
        if "file" not in request.files:
            return {
                "error": "No file provided"
            }, 400

        file = request.files["file"]

        # Check filename
        if file.filename == "":
            return {
                "error": "No file selected"
            }, 400

        # Only allow PDF files
        if not file.filename.lower().endswith(".pdf"):
            return {
                "error": "Only PDF files are allowed"
            }, 400

        filename = secure_filename(file.filename)

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Save uploaded PDF
        file.save(file_path)

        # Open PDF
        pdf = fitz.open(file_path)

        total_pages = len(pdf)
        all_chunks = []

        # Extract and chunk each page separately
        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text")

            page_chunks = chunk_page_text(
                text=text,
                page_number=page_number
            )

            all_chunks.extend(page_chunks)

        pdf.close()

        # Connect to MySQL
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:

                # Insert document
                document_sql = """
                    INSERT INTO documents
                    (filename, file_path)
                    VALUES (%s, %s)
                """

                cursor.execute(
                    document_sql,
                    (filename, file_path)
                )

                document_id = cursor.lastrowid

                # Insert chunks
                chunk_sql = """
                    INSERT INTO chunks
                    (document_id, chunk_text, page_number, embedding)
                    VALUES (%s, %s, %s, %s)
                    """

                for chunk in all_chunks:

                    embedding = generate_embedding(
                        chunk["chunk_text"]
                    )

                    embedding_json = json.dumps(embedding)

                    cursor.execute(
                        chunk_sql,
                        (
                            document_id,
                            chunk["chunk_text"],
                            chunk["page_number"],
                            embedding_json
                        )
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

        return {
            "status": "success",
            "document_id": document_id,
            "filename": filename,
            "total_pages": total_pages,
            "total_chunks": len(all_chunks)
        }

    return app