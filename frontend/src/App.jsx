
import { useEffect, useRef, useState } from "react";
const STORAGE_KEYS = {
  messages: "askdoc_messages",
  document: "askdoc_document",
};

function App() {
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState(null);
  const [documentName, setDocumentName] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const requestLock = useRef(false);
  const fileInputRef = useRef(null);
  const chatAreaRef = useRef(null);

  useEffect(() => {
    try {
      const savedMessages = localStorage.getItem(
        STORAGE_KEYS.messages
      );

      const savedDocument = localStorage.getItem(
        STORAGE_KEYS.document
      );

      if (savedMessages) {
        const parsedMessages = JSON.parse(savedMessages);

        if (Array.isArray(parsedMessages)) {
          setMessages(parsedMessages);
        }
      }

      if (savedDocument) {
        const parsedDocument = JSON.parse(savedDocument);

        if (parsedDocument?.documentId) {
          setDocumentId(parsedDocument.documentId);
        }

        if (parsedDocument?.documentName) {
          setDocumentName(parsedDocument.documentName);
        }
      }
    } catch (error) {
      console.error(
        "Failed to restore AskDoc session:",
        error
      );
    }
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEYS.messages,
        JSON.stringify(messages)
      );
    } catch (error) {
      console.error(
        "Failed to save chat history:",
        error
      );
    }
  }, [messages]);

  useEffect(() => {
    try {
      if (documentId) {
        localStorage.setItem(
          STORAGE_KEYS.document,
          JSON.stringify({
            documentId,
            documentName,
          })
        );
      }
    } catch (error) {
      console.error(
        "Failed to save document:",
        error
      );
    }
  }, [documentId, documentName]);

  useEffect(() => {
    const chatArea = chatAreaRef.current;

    if (!chatArea) {
      return;
    }

    requestAnimationFrame(() => {
      chatArea.scrollTo({
        top: chatArea.scrollHeight,
        behavior: "smooth",
      });
    });
  }, [messages]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {
      setFile(null);
      setDocumentId(null);
      setDocumentName("");
      setUploadMessage("Please select a PDF file.");
      return;
    }

    if (asking || uploading) {
      return;
    }

    setFile(selectedFile);
    setDocumentId(null);
    setDocumentName("");
    setUploadMessage("");
    setMessages([]);
    setQuestion("");

    localStorage.removeItem(
      STORAGE_KEYS.document
    );
  };

  const handleUpload = async () => {
    if (!file || uploading || asking) {
      return;
    }

    setUploading(true);
    setUploadMessage("");

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/documents/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Upload failed."
        );
      }

      const newDocumentId = data.document_id;

      setDocumentId(newDocumentId);
      setDocumentName(file.name);

      setUploadMessage(
        `Document ready • ID ${newDocumentId}`
      );

      setMessages([]);
      setQuestion("");

      // Save immediately.
      localStorage.setItem(
        STORAGE_KEYS.document,
        JSON.stringify({
          documentId: newDocumentId,
          documentName: file.name,
        })
      );

      localStorage.setItem(
        STORAGE_KEYS.messages,
        JSON.stringify([])
      );
    } catch (error) {
      setDocumentId(null);

      setUploadMessage(
        `Upload failed: ${error.message}`
      );
    } finally {
      setUploading(false);
    }
  };

  const handleChangePdf = () => {
    if (uploading || asking) {
      return;
    }

    setFile(null);
    setDocumentId(null);
    setDocumentName("");
    setUploadMessage("");
    setMessages([]);
    setQuestion("");

    localStorage.removeItem(
      STORAGE_KEYS.document
    );

    localStorage.removeItem(
      STORAGE_KEYS.messages
    );

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
      fileInputRef.current.click();
    }
  };

  const handleNewChat = () => {
    if (asking) {
      return;
    }

    setMessages([]);
    setQuestion("");

    localStorage.setItem(
      STORAGE_KEYS.messages,
      JSON.stringify([])
    );
  };

  const handleAskQuestion = async () => {
    if (
      requestLock.current ||
      asking ||
      !question.trim()
    ) {
      return;
    }

    if (!documentId) {
      const message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          "Please upload a document first.",
        sources: [],
        time: new Date().toLocaleTimeString(
          [],
          {
            hour: "2-digit",
            minute: "2-digit",
          }
        ),
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        message,
      ]);

      return;
    }

    requestLock.current = true;
    setAsking(true);

    const userQuestion = question.trim();

    const userMessageId =
      crypto.randomUUID();

    const assistantMessageId =
      crypto.randomUUID();

    const currentTime =
      new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

    setQuestion("");

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        id: userMessageId,
        role: "user",
        content: userQuestion,
        sources: [],
        time: currentTime,
      },
      {
        id: assistantMessageId,
        role: "assistant",
        content: "",
        sources: [],
        time: currentTime,
      },
    ]);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/questions/ask/stream",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            document_id: documentId,
            question: userQuestion,
          }),
        }
      );

      if (!response.ok) {
        let errorMessage =
          "Failed to get answer.";

        try {
          const errorData =
            await response.json();

          errorMessage =
            errorData.message ||
            errorMessage;
        } catch {
          // Keep default message.
        }

        throw new Error(errorMessage);
      }

      if (!response.body) {
        throw new Error(
          "Streaming response is not available."
        );
      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } =
          await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        const lines =
          buffer.split("\n");

        buffer =
          lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) {
            continue;
          }

          let data;

          try {
            data = JSON.parse(line);
          } catch {
            console.error(
              "Invalid streaming JSON:",
              line
            );

            continue;
          }

          if (data.type === "text") {
            setMessages(
              (previousMessages) =>
                previousMessages.map(
                  (message) => {
                    if (
                      message.id !==
                      assistantMessageId
                    ) {
                      return message;
                    }

                    return {
                      ...message,

                      content:
                        message.content +
                        data.content,
                    };
                  }
                )
            );
          }

          if (
            data.type === "sources"
          ) {
            setMessages(
              (previousMessages) =>
                previousMessages.map(
                  (message) => {
                    if (
                      message.id !==
                      assistantMessageId
                    ) {
                      return message;
                    }

                    return {
                      ...message,

                      sources:
                        data.sources ||
                        [],
                    };
                  }
                )
            );
          }

          if (
            data.type === "error"
          ) {
            throw new Error(
              data.message ||
                "Streaming failed."
            );
          }
        }
      }

      buffer += decoder.decode();

      if (buffer.trim()) {
        const remainingLines =
          buffer
            .split("\n")
            .filter(
              (line) => line.trim()
            );

        for (const line of remainingLines) {
          let data;

          try {
            data = JSON.parse(line);
          } catch {
            continue;
          }

          if (
            data.type === "text"
          ) {
            setMessages(
              (previousMessages) =>
                previousMessages.map(
                  (message) => {
                    if (
                      message.id !==
                      assistantMessageId
                    ) {
                      return message;
                    }

                    return {
                      ...message,

                      content:
                        message.content +
                        data.content,
                    };
                  }
                )
            );
          }

          if (
            data.type === "sources"
          ) {
            setMessages(
              (previousMessages) =>
                previousMessages.map(
                  (message) => {
                    if (
                      message.id !==
                      assistantMessageId
                    ) {
                      return message;
                    }

                    return {
                      ...message,

                      sources:
                        data.sources ||
                        [],
                    };
                  }
                )
            );
          }

          if (
            data.type === "error"
          ) {
            throw new Error(
              data.message ||
                "Streaming failed."
            );
          }
        }
      }
    } catch (error) {
      setMessages(
        (previousMessages) =>
          previousMessages.map(
            (message) => {
              if (
                message.id !==
                assistantMessageId
              ) {
                return message;
              }

              return {
                ...message,

                content:
                  `Error: ${error.message}`,

                sources: [],
              };
            }
          )
      );
    } finally {
      requestLock.current = false;
      setAsking(false);
    }
  };

  const userMessages =
    messages.filter(
      (message) =>
        message.role === "user"
    );

  const isDocumentReady =
    Boolean(documentId);

  const displayedDocumentName =
    file?.name ||
    documentName ||
    "Uploaded document.pdf";

  return (
    <div className="app-shell">

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <aside className="sidebar">

        {/* BRAND */}

        <div className="brand">
          <div className="brand-icon">
            <img src="/AskDoc_logo.jpeg" alt="AskDoc logo" />
          </div>

          <div className="brand-text">
            <h1>AskDoc</h1>
            <p>AI Document Analyzer</p>
          </div>

        </div>

        {/* NEW CHAT */}

        <button
          className="new-chat-button"
          type="button"
          onClick={handleNewChat}
          disabled={asking}
        >
          <span className="plus-icon">
            ＋
          </span>

          <span>
            New Chat
          </span>
        </button>

        {/* CHAT HISTORY */}

        <div className="sidebar-section chat-section">

          <div className="sidebar-section-title">

            <span className="section-icon">
              ▢
            </span>

            <span>
              Chats
            </span>

          </div>

          <div className="chat-history">

            {userMessages.length >
            0 ? (
              userMessages.map(
                (message) => (
                  <div
                    className="history-item"
                    key={message.id}
                    title={
                      message.content
                    }
                  >
                    <span className="history-question">
                      {message.content}
                    </span>

                    <span className="history-time">
                      {message.time ||
                        ""}
                    </span>
                  </div>
                )
              )
            ) : (
              <div className="empty-history">
                Start a conversation
                with your document.
              </div>
            )}

          </div>

        </div>

        {/* UPLOADED DOCUMENT */}

        <div className="sidebar-section document-section">

          <div className="sidebar-section-title">

            <span className="section-icon">
              ▤
            </span>

            <span>
              Uploaded Document
            </span>

          </div>

          {isDocumentReady ? (
            <>
              <div className="document-card document-ready">

                <div className="pdf-icon">
                  PDF
                </div>

                <div className="document-info">

                  <strong
                    className="document-name"
                    title={
                      displayedDocumentName
                    }
                  >
                    {
                      displayedDocumentName
                    }
                  </strong>

                  <span className="document-pages">
                    Document ready for
                    Q&A
                  </span>

                </div>

                <div className="document-check is-ready">
                  ✓
                </div>

              </div>

              {uploadMessage && (
                <div className="upload-status success">

                  <span>
                    ✓
                  </span>

                  <span>
                    {uploadMessage}
                  </span>

                </div>
              )}

              <button
                className="change-pdf-button"
                type="button"
                onClick={
                  handleChangePdf
                }
                disabled={
                  uploading ||
                  asking
                }
              >
                <span>
                  ↗
                </span>

                Change PDF
              </button>
            </>
          ) : file ? (
            <>
              <div className="document-card document-selected">

                <div className="pdf-icon">
                  PDF
                </div>

                <div className="document-info">

                  <strong
                    className="document-name"
                    title={file.name}
                  >
                    {file.name}
                  </strong>

                  <span className="document-pages">
                    {uploading
                      ? "Uploading document..."
                      : "Ready to upload"}
                  </span>

                </div>

                <div
                  className={`document-check ${
                    uploading
                      ? "is-loading"
                      : "is-pending"
                  }`}
                >
                  {uploading
                    ? "..."
                    : "•"}
                </div>

              </div>

              {uploadMessage && (
                <div
                  className={`upload-status ${
                    uploadMessage.startsWith(
                      "Upload failed"
                    )
                      ? "error"
                      : "success"
                  }`}
                >
                  <span>
                    {uploadMessage.startsWith(
                      "Upload failed"
                    )
                      ? "!"
                      : "✓"}
                  </span>

                  <span>
                    {uploadMessage}
                  </span>
                </div>
              )}
            </>
          ) : (
            <div className="no-document">

              <span className="no-document-icon">
                +
              </span>

              <div>

                <strong>
                  No document yet
                </strong>

                <p>
                  Select a PDF to begin.
                </p>

              </div>

            </div>
          )}

        </div>

        {/* UPLOAD */}

        {!isDocumentReady && (
          <div className="sidebar-upload">

            <label
              htmlFor="pdf-upload"
              className={`select-pdf-button ${
                uploading ||
                asking
                  ? "disabled"
                  : ""
              }`}
            >
              <span>
                ＋
              </span>

              {file
                ? "Choose Another PDF"
                : "Select PDF"}
            </label>

            <input
              ref={fileInputRef}
              id="pdf-upload"
              className="hidden-file-input"
              type="file"
              accept=".pdf,application/pdf"
              onChange={
                handleFileChange
              }
              disabled={
                uploading ||
                asking
              }
            />

            {file && (
              <button
                className="sidebar-upload-button"
                type="button"
                onClick={
                  handleUpload
                }
                disabled={
                  uploading ||
                  asking
                }
              >
                {uploading ? (
                  <>
                    <span className="button-spinner"></span>

                    Processing PDF...
                  </>
                ) : (
                  <>
                    Upload Document

                    <span>
                      →
                    </span>
                  </>
                )}
              </button>
            )}

          </div>
        )}

        {/* SYSTEM STATUS */}

        <div className="sidebar-bottom">

          <div className="system-card">

            <span className="online-dot"></span>

            <div>

              <strong>
                System Online
              </strong>

              <span>
                RAG • Groq LLM
              </span>

            </div>

          </div>

        </div>

      </aside>

      {/* =====================================================
          MAIN PANEL
      ===================================================== */}

      <main className="main-panel">

        {/* TOP BAR */}

        <header className="topbar">

            <div className="topbar-title">

              <div className="topbar-logo">
                <img
                  src="/AskDoc_logo.jpeg"
                  alt="AskDoc"
                />
              </div>

              <div>
                <h2>AskDoc</h2>

                <span className="topbar-subtitle">
                  AI document analyzer
                </span>
              </div>

            </div>

          <div
            className={`document-indicator ${
              isDocumentReady
                ? "ready"
                : ""
            }`}
          >

            <span></span>

            {isDocumentReady
              ? "Document ready"
              : "No document"}

          </div>

        </header>

        {/* CHAT AREA */}

        <section
          className="chat-area"
          ref={chatAreaRef}
        >

          {/* WELCOME */}

          {messages.length ===
            0 && (
            <div className="welcome-card">

              <div className="welcome-icon">

            <div className="brand-logo">
              <img
                src="/AskDoc_logo.jpeg"
                alt="AskDoc"
              />
            </div>

              </div>

              <div>

                <h2>
                  Welcome to AskDoc
                </h2>

                <p>
                  Upload a document
                  and ask questions
                  about its contents.
                </p>

              </div>

            </div>
          )}

          {/* EMPTY STATE */}

          {messages.length ===
            0 && (
            <div className="empty-main">

              <div className="empty-main-icon">
                {isDocumentReady
                  ? "✓"
                  : "✦"}
              </div>

              <h2>
                {isDocumentReady
                  ? "Your document is ready"
                  : "Start with a document"}
              </h2>

              <p>
                {isDocumentReady
                  ? "Ask anything about your uploaded PDF."
                  : "Select and upload a PDF from the sidebar to start asking questions."}
              </p>

              {isDocumentReady && (
                <div className="ready-badge">

                  <span></span>

                  Ready for questions

                </div>
              )}

            </div>
          )}

          {/* MESSAGES */}

          <div className="messages">

            {messages.map(
              (message) => {

                const isUser =
                  message.role ===
                  "user";

                return (
                  <div
                    key={
                      message.id
                    }
                    className={`message-row ${
                      isUser
                        ? "user-row"
                        : "assistant-row"
                    }`}
                  >

                    {/* AI AVATAR */}

                    {!isUser && (
                      <div className="ai-avatar">
                        <img
                          src="/AskDoc_logo.jpeg"
                          alt="AskDoc AI"
                        />
                      </div>
                    )}

                    {/* MESSAGE */}

                    <div className="message-wrapper">

                      <div
                        className={`message-bubble ${
                          isUser
                            ? "user-bubble"
                            : "assistant-bubble"
                        }`}
                      >

                        {message.role ===
                          "assistant" &&
                        !message.content ? (
                          <div className="thinking">

                            <span></span>
                            <span></span>
                            <span></span>

                          </div>
                        ) : (
                          <div className="message-text">
                            {
                              message.content
                            }
                          </div>
                        )}

                        {message.time && (
                          <div className="message-time">
                            {
                              message.time
                            }
                          </div>
                        )}

                      </div>

                      {/* SOURCES */}

                      {!isUser &&
                        message.sources &&
                        message.sources
                          .length >
                          0 && (
                          <div className="sources-container">

                            <span className="sources-title">
                              Sources
                            </span>

                            <div className="sources-list">

                              {message.sources.map(
                                (
                                  source,
                                  sourceIndex
                                ) => (
                                  <span
                                    className="source-button"
                                    key={`${message.id}-source-${sourceIndex}`}
                                  >
                                    Page{" "}
                                    {
                                      source.page_number
                                    }
                                  </span>
                                )
                              )}

                            </div>

                          </div>
                        )}

                    </div>

                    {/* USER AVATAR */}

                    {isUser && (
                      <div className="user-message-avatar">
                        <span>
                          U
                        </span>
                      </div>
                    )}

                  </div>
                );
              }
            )}

          </div>

          <div className="chat-bottom-anchor"></div>

        </section>

        {/* INPUT */}

        <div className="input-section">

          <div
            className={`input-container ${
              !isDocumentReady
                ? "input-disabled"
                : ""
            }`}
          >

            <span className="attach-icon">
              ✦
            </span>

            <input
              type="text"
              value={question}
              placeholder={
                isDocumentReady
                  ? "Ask a question about your document..."
                  : "Upload a document first..."
              }
              onChange={(event) =>
                setQuestion(
                  event.target.value
                )
              }
              onKeyDown={(event) => {

                if (
                  event.key ===
                    "Enter" &&
                  !event.shiftKey
                ) {
                  event.preventDefault();

                  if (!asking) {
                    handleAskQuestion();
                  }
                }

              }}
              disabled={
                !isDocumentReady ||
                asking
              }
            />

            <button
              className="send-button"
              type="button"
              onClick={
                handleAskQuestion
              }
              disabled={
                !isDocumentReady ||
                !question.trim() ||
                asking
              }
              aria-label="Send question"
            >
              {asking ? (
                <span className="send-spinner"></span>
              ) : (
                "➤"
              )}
            </button>

          </div>

          <p className="input-hint">
            AskDoc answers using only
            your uploaded document.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;

