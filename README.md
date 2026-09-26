AskDoc — AI Document Q&A Platform

Ask questions about your documents and get grounded answers with page-level citations.

AskDoc is a full-stack AI document question-answering platform built around a Retrieval-Augmented Generation (RAG) pipeline. Users can upload documents, process their content into searchable chunks, retrieve relevant information using local embeddings and cosine similarity, and ask questions through a conversational interface.

The system is designed to keep document retrieval grounded in the uploaded content and provide page-level citations with generated answers.

✨ Features

📄 Document upload and processing

✂️ Text extraction and document chunking

🧠 Local semantic embeddings using Sentence Transformers

🔎 Similarity-based document retrieval using cosine similarity

🤖 AI-powered question answering with Groq

📑 Page-level citations for retrieved information

💬 Conversational Q&A interface

🚫 Out-of-scope question handling when information is not found in the document

⚡ Streaming responses for interactive answers

🗄️ MySQL database integration

🔌 Flask REST API backend

⚛️ React frontend with Vite

🧪 Backend tests using Pytest

🔐 Environment-based configuration for API credentials

📱 Responsive user interface

🧠 How AskDoc Works

                    ┌─────────────────────┐
                    │   User uploads PDF  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Extraction   │
                    │      PyMuPDF        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Chunking       │
                    │   Document Text     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Embeddings       │
                    │ all-MiniLM-L6-v2    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   MySQL Storage     │
                    │ Documents + Vectors │
                    └──────────┬──────────┘
                               │
                    User asks a question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Query Embedding     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Similarity Search   │
                    │  Cosine Similarity  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Chunks     │
                    │ + Page References   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Groq LLM         │
                    │ Grounded Generation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Citations  │
                    └─────────────────────┘

🛠️ Technology Stack

Frontend

React 19

JavaScript

Vite

CSS

Backend

Python

Flask

PyMySQL

REST APIs

AI / RAG

Sentence Transformers

all-MiniLM-L6-v2

NumPy

Cosine similarity

Groq

Document Processing

PyMuPDF

Database

MySQL

Testing

Pytest

📁 Project Structure

AskDoc/
│
├── backend/
│   ├── app/
│   │   ├── chunking.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── embeddings.py
│   │   ├── rag.py
│   │   ├── retrieval.py
│   │   └── __init__.py
│   │
│   ├── tests/
│   ├── uploads/
│   ├── generate_embeddings.py
│   ├── requirements.txt
│   └── run.py
│
├── database/
│   └── schema.sql
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md

⚙️ Requirements

Before running AskDoc, install:

Python 3.10+

Node.js 18+

npm

MySQL 8+

A Groq API key

🚀 Installation

1. Clone the repository

git clone https://github.com/HassanCodeHub/AskDoc.git
cd AskDoc

2. Backend setup

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

3. Configure environment variables

Create:

backend/.env

Add your local configuration and API credentials.

Do not commit .env to GitHub.

4. Configure MySQL

Create the AskDoc database and run:

database/schema.sql

Then configure the database connection in your environment variables.

5. Start the backend

From:

backend/

run:

python run.py

The Flask API will start locally.

6. Start the frontend

Open a second terminal:

cd frontend
npm install
npm run dev

Open the local Vite URL shown in the terminal.

🔌 API

AskDoc provides REST endpoints for document processing and question answering.

The backend supports:

Document upload

Document retrieval

Question answering

Streaming question responses

Health/status checks

Refer to the backend route implementation for the current endpoint definitions.

🧪 Testing

Backend tests can be executed from the backend directory:

pytest

Individual test files are also available for:

Groq connectivity

Document retrieval

RAG behavior

End-to-end document Q&A

Streaming responses

🔐 Security & Privacy

API credentials are stored using environment variables.

.env files are excluded from version control.

Uploaded documents are kept outside the public repository.

Database credentials should never be committed to GitHub.

🎯 Project Goals

AskDoc was built to demonstrate practical implementation of:

Retrieval-Augmented Generation

Semantic document search

Local embedding generation

Vector similarity retrieval

LLM-based grounded responses

Full-stack application architecture

REST API development

React frontend development

MySQL data persistence

📌 Current Limitations

AskDoc is a portfolio and learning project. Retrieval quality depends on document structure, chunking strategy, embedding quality, and the selected similarity threshold.

The system should not be treated as a source of professional, legal, medical, financial, or other high-stakes advice.

🔮 Future Improvements

Support for additional document formats

Improved chunking strategies

Persistent vector database integration

Authentication and user accounts

Document management dashboard

Improved conversation history

Retrieval evaluation metrics

Production deployment

👨‍💻 Author

Hassan

BCA Student · Full-Stack Developer

GitHub: HassanCodeHub