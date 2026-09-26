import os
import re

from dotenv import load_dotenv
from groq import Groq

from .retrieval import retrieve_chunks


load_dotenv()


def build_rag_prompt(question, retrieved_chunks):
    """
    Build a prompt that forces the LLM to answer
    using only the retrieved document context.
    """

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"[Page {chunk['page_number']}]\n"
            f"{chunk['chunk_text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the document context below.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer cannot be found in the provided context,
   say: "I couldn't find that information in the uploaded document."
4. Every factual statement must include its source page
   in the format [Page X].
5. Keep the answer concise and directly answer the question.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

ANSWER:
"""

    return prompt

def stream_groq_answer(prompt):
    """
    Stream the Groq GPT-OSS response.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in .env"
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document question-answering assistant. "
                    "Answer the user's question using ONLY the supplied "
                    "document context. "
                    "If the answer is present in the context, answer clearly "
                    "and concisely. "
                    "Cite the relevant page using [Page X]. "
                    "If the answer is not present, say that you could not "
                    "find the information in the document."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=1,
        reasoning_effort="low",
        max_completion_tokens=1024,
        stream=True
    )

    for chunk in response:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        content = delta.content

        if content:
            yield content

def prepare_streaming_rag(question, top_k=3, document_id=None):
    """
    Retrieve document chunks and prepare the RAG prompt
    for streaming generation.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    retrieved_chunks = retrieve_chunks(
        query=question,
        top_k=top_k,
        document_id=document_id
    )

    if not retrieved_chunks:
        return None, []

    prompt = build_rag_prompt(
        question,
        retrieved_chunks
    )

    return prompt, retrieved_chunks

def ask_document(question, top_k=3, document_id=None):
    """
    Retrieve relevant document chunks and ask Groq
    to generate a grounded answer.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    # Step 1: Retrieve relevant chunks
    retrieved_chunks = retrieve_chunks(
        query=question,
        top_k=top_k,
        document_id=document_id

    )

    # Step 2: Make sure we actually found context
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find relevant information in the uploaded document.",
            "sources": []
        }

    # Step 3: Build the RAG prompt
    prompt = build_rag_prompt(
        question,
        retrieved_chunks
    )

    # Step 4: Load Groq API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in .env"
        )

    client = Groq(api_key=api_key)

    # Step 5: Ask Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions about uploaded "
                    "documents using only the supplied context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    # Step 6: Extract the page numbers actually cited by the LLM
    cited_pages = set(
        int(page)
        for page in re.findall(r"\[Page\s+(\d+)\]", answer)
    )

    # Keep only retrieved chunks from pages cited in the answer
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

    return {
        "answer": answer,
        "sources": sources
    }