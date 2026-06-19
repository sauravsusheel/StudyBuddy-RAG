# StudyBuddy RAG — Architecture & Knowledge Graph

## Project Structure

```
StudyBuddy RAG/
├── app.py                    # Flask backend — core RAG engine
├── requirements.txt          # Python dependencies
├── .env                      # API key (gitignored)
├── .env.example              # Template for .env
├── .gitignore                # Git exclusions
├── README.md                 # User guide
├── ARCHITECTURE.md           # This file
├── start.bat                 # Windows startup script
├── static/
│   ├── index.html            # App shell & UI structure
│   ├── style.css             # Notion-style theming
│   └── app.js                # Frontend logic & state management
├── uploads/                  # Temporary file storage (auto-created)
├── vectorstores/             # Reserved for future persistence (auto-created)
└── venv/                      # Python virtual environment (gitignored)
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ index.html (Notion-style UI)                             │   │
│  │ ├─ Sidebar: Model selector, API status, file info       │   │
│  │ ├─ Drop zone: Drag-and-drop file upload                 │   │
│  │ └─ Chat area: Messages, citations, thinking indicator   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ↕ (HTTP)                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ app.js (Frontend Logic)                                  │   │
│  │ ├─ File validation & upload handling                     │   │
│  │ ├─ Session state management                              │   │
│  │ ├─ Chat message rendering                                │   │
│  │ └─ Citation display & toggle                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                           ↕ (REST API)
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (app.py)                        │
│                                                                   │
│  ┌─ POST /api/upload ──────────────────────────────────────┐   │
│  │ 1. Receive file (PDF/DOCX/PPTX/Image)                   │   │
│  │ 2. Route to appropriate extractor:                       │   │
│  │    ├─ extract_pdf() → pypdf                              │   │
│  │    ├─ extract_docx() → python-docx                       │   │
│  │    ├─ extract_pptx() → python-pptx                       │   │
│  │    └─ extract_image_via_vision() → GPT-4o Vision         │   │
│  │ 3. chunk_pages() → 800-char overlapping chunks           │   │
│  │ 4. embed_texts() → text-embedding-3-small via OpenRouter │   │
│  │ 5. Store in sessions[session_id] (in-memory)             │   │
│  │ 6. Return: session_id, file_name, chunk_count            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─ POST /api/chat ────────────────────────────────────────┐   │
│  │ 1. Receive: session_id, question, model                  │   │
│  │ 2. Embed query → text-embedding-3-small                  │   │
│  │ 3. cosine_top_k() → retrieve top-4 chunks                │   │
│  │ 4. Build context from chunks                             │   │
│  │ 5. Call LLM via OpenRouter:                              │   │
│  │    ├─ System prompt: "You are StudyBuddy tutor"          │   │
│  │    ├─ User prompt: context + question                    │   │
│  │    └─ Model: user-selected (default: Llama 3.1 8B)       │   │
│  │ 6. Extract answer + build citations                      │   │
│  │ 7. Return: answer, citations[], model                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─ DELETE /api/session/<id> ──────────────────────────────┐   │
│  │ 1. Remove from sessions dict                             │   │
│  │ 2. Clean up uploaded files                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─ In-Memory Data Store ──────────────────────────────────┐   │
│  │ sessions = {                                             │   │
│  │   "uuid-1": {                                            │   │
│  │     "chunks": [{page, text, chunk_id}, ...],             │   │
│  │     "embeddings": np.ndarray (N, 1536),                  │   │
│  │     "file_name": "document.pdf",                         │   │
│  │     "file_type": "PDF"                                   │   │
│  │   },                                                      │   │
│  │   "uuid-2": { ... }                                      │   │
│  │ }                                                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                           ↕ (HTTPS)
┌─────────────────────────────────────────────────────────────────┐
│                    OPENROUTER API                                │
│  ├─ text-embedding-3-small (embeddings)                         │
│  ├─ openai/gpt-4o (image vision)                                │
│  └─ User-selected LLM (chat completion)                         │
│     ├─ meta-llama/llama-3.1-8b-instruct                         │
│     ├─ meta-llama/llama-3.1-70b-instruct                        │
│     ├─ google/gemma-3-27b-it                                    │
│     ├─ mistralai/mistral-7b-instruct                            │
│     ├─ openai/gpt-4o                                            │
│     ├─ anthropic/claude-3.5-sonnet                              │
│     └─ ... (10 total options)                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Interactions

### 1. **File Upload Pipeline**

```
User drops file
    ↓
app.js: handleFileSelect()
    ↓
Validate extension (PDF/DOCX/PPTX/Image)
    ↓
POST /api/upload (FormData: file + session context)
    ↓
app.py: upload_file()
    ├─ Save to uploads/
    ├─ Route by extension:
    │  ├─ PDF → extract_pdf() → pypdf.PdfReader
    │  ├─ DOCX → extract_docx() → python-docx.Document
    │  ├─ PPTX → extract_pptx() → python-pptx.Presentation
    │  └─ Image → extract_image_via_vision() → GPT-4o Vision
    ├─ chunk_pages() → RecursiveCharacterTextSplitter logic
    ├─ embed_texts() → OpenRouter embeddings API
    ├─ Store in sessions[session_id]
    └─ Return JSON: {session_id, file_name, chunk_count, ...}
    ↓
app.js: Update UI
    ├─ Show file status (green dot + name)
    ├─ Enable chat input
    └─ Clear previous messages
```

### 2. **Chat & RAG Pipeline**

```
User types question + presses Enter
    ↓
app.js: sendMessage()
    ├─ Validate: question, sessionId, model
    ├─ Show thinking indicator
    └─ POST /api/chat (JSON: {session_id, question, model})
    ↓
app.py: chat()
    ├─ Embed query → OpenRouter embeddings
    ├─ cosine_top_k() → numpy dot product search
    │  └─ Retrieve top-4 most similar chunks
    ├─ Build context string from chunks
    ├─ Call LLM via OpenRouter:
    │  ├─ System: "You are StudyBuddy tutor..."
    │  ├─ User: "[Source 1 — Page X]\n{chunk}\n...\n\nQuestion: {q}"
    │  └─ Model: user-selected
    ├─ Extract answer from response
    ├─ Build citations array:
    │  └─ For each chunk: {source_num, page, snippet, file_name}
    └─ Return JSON: {answer, citations[], model}
    ↓
app.js: Render response
    ├─ Remove thinking indicator
    ├─ Display assistant message
    ├─ Show collapsible citations panel
    │  └─ Each citation: badge + page + snippet
    └─ Scroll to bottom
```

### 3. **Embedding & Similarity Search**

```
Text chunks (800 chars each, 150-char overlap)
    ↓
embed_texts(client, texts)
    ├─ Batch by 512 items
    ├─ Call OpenRouter: POST /embeddings
    │  └─ Model: text-embedding-3-small
    │  └─ Returns: 1536-dim vectors
    ├─ Stack into numpy array (N, 1536)
    ├─ L2-normalize each vector
    └─ Return: normalized embeddings
    ↓
Query embedding (same process)
    ↓
cosine_top_k(query_vec, doc_vecs, k=4)
    ├─ Compute: doc_vecs @ query_vec (dot product)
    ├─ Sort scores descending
    └─ Return: indices of top-4 chunks
    ↓
Retrieve chunks by index
    ↓
Build context for LLM
```

---

## File Type Support Matrix

| Format | Parser | Output | Use Case |
|---|---|---|---|
| **PDF** | pypdf | Text per page | Documents, papers, reports |
| **DOCX** | python-docx | Paragraphs + tables | Word docs, essays |
| **PPTX** | python-pptx | Text per slide | Presentations, lectures |
| **PNG/JPG/WEBP/GIF/BMP** | PIL + GPT-4o Vision | OCR + description | Diagrams, charts, handwritten notes |

---

## Session Lifecycle

```
1. User uploads file
   └─ session_id = uuid.uuid4()
   └─ sessions[session_id] = {chunks, embeddings, file_name, file_type}

2. User asks questions (multiple)
   └─ Same session_id used for all queries
   └─ Embeddings reused (no re-embedding)

3. User clears session or uploads new file
   └─ DELETE /api/session/{session_id}
   └─ Remove from sessions dict
   └─ Delete uploaded file from disk
   └─ Create new session_id for next upload
```

---

## Dependencies & Their Roles

| Package | Version | Purpose |
|---|---|---|
| `flask` | 3.1.0 | Web server & routing |
| `flask-cors` | 5.0.0 | Cross-origin requests |
| `pypdf` | 5.4.0 | PDF text extraction |
| `python-docx` | 1.1.2 | DOCX parsing |
| `python-pptx` | 1.0.2 | PPTX parsing |
| `pillow` | 12.2.0 | Image resizing & encoding |
| `openai` | 1.82.0 | OpenRouter API client |
| `numpy` | 2.4.4 | Cosine similarity search |
| `python-dotenv` | 1.1.0 | Load .env secrets |
| `werkzeug` | 3.1.3 | WSGI utilities |

---

## Security & Privacy

- **API Key**: Stored in `.env` (gitignored), never exposed to frontend
- **File Storage**: Temporary, deleted after session ends
- **Embeddings**: Stored in-memory only, lost on server restart
- **No Cloud**: All processing local except API calls to OpenRouter
- **No Logging**: User queries not logged or stored

---

## Performance Characteristics

| Operation | Time | Notes |
|---|---|---|
| PDF upload (10 pages) | ~2-5s | Depends on text density |
| DOCX upload | ~1-2s | Faster than PDF |
| PPTX upload | ~1-2s | Per slide |
| Image upload | ~3-8s | Vision model inference |
| Embedding 100 chunks | ~1-2s | Batched API calls |
| Query search | <100ms | Numpy dot product |
| LLM response | ~2-10s | Depends on model & length |

---

## Future Enhancements

- [ ] Persistent vector store (FAISS on disk)
- [ ] Multi-file sessions (upload multiple PDFs)
- [ ] Conversation history
- [ ] Export chat as PDF
- [ ] User authentication
- [ ] Rate limiting
- [ ] Streaming responses
- [ ] Custom system prompts
- [ ] Reranking (cross-encoder)
- [ ] Hybrid search (BM25 + semantic)
