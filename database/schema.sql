CREATE DATABASE IF NOT EXISTS smart_document_qa;

USE smart_document_qa;


-- Stores information about uploaded documents
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Stores chunks extracted from documents
CREATE TABLE chunks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    document_id INT NOT NULL,

    chunk_text TEXT NOT NULL,

    page_number INT NOT NULL,

    embedding JSON NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE
);