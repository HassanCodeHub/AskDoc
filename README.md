# AskDoc — AI Document Q&A Platform

> **Ask questions about your documents and get grounded answers with page-level citations.**

AskDoc is a full-stack **AI Document Question-Answering platform** built around a Retrieval-Augmented Generation (RAG) pipeline.

It allows users to upload documents, extract and chunk their content, generate local semantic embeddings, retrieve relevant information using cosine similarity, and ask questions through a conversational interface.

The system is designed to keep generated answers **grounded in the uploaded document content** while providing **page-level references** for retrieved information.

---

## 📸 Project Preview

<!-- Keep your existing screenshots here -->

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Landing_page.png" alt="AskDoc Dashboard" width="900"/>
</p>

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Document_ready.png" alt="AskDoc Document Q&A" width="900"/>
</p>

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Upload_page.png" alt="AskDoc Document Q&A" width="900"/>
</p>

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Question_input.png" alt="AskDoc Document Q&A" width="900"/>
</p>

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Loading_response.png" alt="AskDoc Document Q&A" width="900"/>
</p>

<p align="center">
  <img src="C:\codings\AskDoc\screenshots\Chat_response.png" alt="AskDoc Document Q&A" width="900"/>
</p>

---

## ✨ Features

| Feature                           | Description                                                       |
| --------------------------------- | ----------------------------------------------------------------- |
| 📄 **Document Upload**            | Upload documents for processing and question answering            |
| ✂️ **Text Extraction & Chunking** | Extract document content and divide it into searchable chunks     |
| 🧠 **Local Embeddings**           | Generate semantic embeddings using Sentence Transformers          |
| 🔎 **Semantic Retrieval**         | Retrieve relevant chunks using cosine similarity                  |
| 🤖 **AI Question Answering**      | Generate grounded answers using Groq                              |
| 📑 **Page-Level Citations**       | Reference the pages containing retrieved information              |
| 💬 **Conversational Interface**   | Ask multiple questions through an interactive chat interface      |
| 🚫 **Out-of-Scope Handling**      | Avoid generating answers when relevant information is unavailable |
| ⚡ **Streaming Responses**         | Stream generated answers for a more interactive experience        |
| 🗄️ **MySQL Integration**         | Persist application and document-related data                     |
| 🔌 **REST API**                   | Flask-powered backend API                                         |
| ⚛️ **React Frontend**             | Responsive frontend built with React and Vite                     |
| 🧪 **Automated Testing**          | Backend testing using Pytest                                      |
| 🔐 **Environment Configuration**  | Secure API credential configuration through environment variables |
| 📱 **Responsive UI**              | Designed for different screen sizes                               |

---

## 🧠 How AskDoc Works

AskDoc follows a Retrieval-Augmented Generation workflow:

```text
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
                    │     Embeddings      │
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
                    │   Query Embedding   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Similarity Search │
                    │   Cosine Similarity │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Relevant Chunks   │
                    │   + Page References│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Groq LLM       │
                    │ Grounded Generation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Answer + Citations │
                    └─────────────────────┘
```

### 🔄 RAG Pipeline

**1. Upload** → User uploads a document.

**2. Extract** → PyMuPDF extracts the document text while preserving page information.

**3. Chunk** → Extracted content is divided into smaller searchable chunks.

**4. Embed** → Sentence Transformers converts chunks into semantic vectors.

**5. Store** → Document data, chunks, embeddings, and references are persisted.

**6. Retrieve** → The user's question is converted into an embedding and compared against stored document vectors.

**7. Generate** → Relevant chunks are provided to the Groq-powered LLM as context.

**8. Cite** → The generated response includes page-level references to the retrieved document content.

---

## 🛠️ Technology Stack

### Frontend

* **React 19**
* **JavaScript**
* **Vite**
* **CSS**

### Backend

* **Python**
* **Flask**
* **PyMySQL**
* **REST APIs**

### AI / RAG

* **Sentence Transformers**
* **all-MiniLM-L6-v2**
* **NumPy**
* **Cosine Similarity**
* **Groq**

### Document Processing

* **PyMuPDF**

### Database

* **MySQL**

### Testing

* **Pytest**

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────┐
│                    React Frontend                   │
│                                                     │
│  Upload Documents  │  Chat Interface  │  Citations │
└───────────────────────┬─────────────────────────────┘
                        │
                        │ REST API
                        ▼
┌─────────────────────────────────────────────────────┐
│                    Flask Backend                    │
│                                                     │
│  Document Processing │ Retrieval │ RAG │ Streaming  │
└──────────────┬───────────────────────────┬──────────┘
               │                           │
               ▼                           ▼
┌─────────────────────────┐    ┌──────────────────────┐
│     Sentence           │    │        Groq LLM       │
│     Transformers       │    │  Grounded Generation  │
│     Embeddings         │    └──────────────────────┘
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│                       MySQL                         │
│                                                     │
│  Documents │ Chunks │ Embeddings │ Page References │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
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
```

---

## ⚙️ Requirements

Before running AskDoc, make sure you have:

* Python **3.10+**
* Node.js **18+**
* npm
* MySQL **8+**
* Groq API key

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/HassanCodeHub/AskDoc.git
cd AskDoc
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv .venv
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory:

```text
backend/.env
```

Add your local configuration and API credentials.

> ⚠️ Never commit your `.env` file or expose API credentials publicly.

---

### 4. Configure MySQL

Create the AskDoc database and execute:

```text
database/schema.sql
```

Then configure the database connection through your environment variables.

---

### 5. Start the Backend

From the `backend` directory:

```bash
python run.py
```

The Flask API will start locally.

---

### 6. Start the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite URL displayed in the terminal.

---

## 🔌 API

AskDoc exposes REST endpoints for document processing and question answering.

The backend currently supports:

* 📄 Document upload
* 🔎 Document retrieval
* 🤖 Question answering
* ⚡ Streaming question responses
* ❤️ Health/status checks

For the exact endpoint definitions, refer to the current Flask route implementation in the backend.

---

## 🧪 Testing

Navigate to the backend directory and run:

```bash
pytest
```

The project includes tests covering areas such as:

* Groq connectivity
* Document retrieval
* RAG behavior
* End-to-end document Q&A
* Streaming responses

---

## 🔐 Security & Privacy

AskDoc follows several basic security practices:

* 🔑 API credentials are stored using environment variables.
* 🚫 `.env` files are excluded from version control.
* 📂 Uploaded documents are kept outside the public repository.
* 🗄️ Database credentials should never be committed to GitHub.

> **Important:** Never push API keys, database passwords, or private documents to a public repository.

---

## 🎯 Project Goals

AskDoc was developed to demonstrate practical implementation of:

* Retrieval-Augmented Generation
* Semantic document search
* Local embedding generation
* Vector similarity retrieval
* Grounded LLM responses
* Full-stack application architecture
* REST API development
* React frontend development
* MySQL data persistence
* Automated backend testing

---

## 📌 Current Limitations

AskDoc is currently a **portfolio and learning project**.

Retrieval quality can depend on:

* Document structure
* Chunking strategy
* Embedding quality
* Similarity threshold
* Quality and relevance of the uploaded content

AskDoc should **not** be treated as a source of professional, legal, medical, financial, or other high-stakes advice.

---

## 🔮 Future Improvements

Planned improvements include:

* 📄 Support for additional document formats
* 🧩 Improved document chunking strategies
* 🗃️ Persistent vector database integration
* 🔐 Authentication and user accounts
* 📚 Document management dashboard
* 💬 Improved conversation history
* 📊 Retrieval evaluation metrics
* ☁️ Production deployment

---

## 👨‍💻 Author

### Hassan

**BCA Student · Full-Stack Developer**

Building practical digital experiences with code and creativity.

🔗 **GitHub:** [HassanCodeHub](https://github.com/HassanCodeHub)

---

## ⭐ Support

If you find AskDoc interesting or useful, consider giving the repository a ⭐ on GitHub.

---

<p align="center">
  <b>AskDoc — Ask your documents. Get grounded answers.</b>
</p>
