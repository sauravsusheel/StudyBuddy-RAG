# 📚 About StudyBuddy RAG

## What is StudyBuddy RAG?

**StudyBuddy RAG** is an open-source, AI-powered document analysis and tutoring application that leverages Retrieval-Augmented Generation (RAG) to transform any document into an intelligent study companion. Upload a PDF, Word document, PowerPoint presentation, or image—and ask questions about it. StudyBuddy will find the exact source material and provide accurate, cited answers.

---

## 🎯 Mission

To democratize access to personalized learning by making it easy for students, professionals, and organizations to ask intelligent questions about any document and receive source-cited answers powered by state-of-the-art language models.

---

## ✨ Key Features

### 📄 Universal Document Support
- **PDF** — Extracts text page-by-page using pypdf
- **Word (DOCX/DOC)** — Parses paragraphs, tables, and formatting via python-docx
- **PowerPoint (PPTX)** — Reads slide text and content with python-pptx
- **Images (PNG/JPG/WEBP/GIF/BMP)** — Optical character recognition (OCR) + visual description via GPT-4o Vision

### 🧠 Intelligent RAG Pipeline
- **Text Chunking** — Splits documents into semantically meaningful 800-character overlapping chunks
- **Vector Embeddings** — Uses `text-embedding-3-small` from OpenRouter for semantic search
- **Similarity Search** — Pure NumPy cosine similarity (no FAISS dependency) for instant retrieval
- **Context-Aware Responses** — Sends top-4 relevant chunks to the LLM for accurate, grounded answers

### 🎯 Source Citations
Every answer includes:
- **Source Badge** — Which reference (1-4) was used
- **Page Number** — Exact location in the source document
- **Text Snippet** — Direct quote from the document (300 chars)
- **File Reference** — Original filename

### 🤖 Multi-Model Support
Choose from 10+ language models via OpenRouter:
- **Open Models**: Llama 3.1 (8B/70B), Mistral 7B, Mixtral 8x7B, Gemma 3
- **Proprietary**: GPT-4o, Claude 3.5 Sonnet, Claude 3 Haiku
- **Swap models mid-session** — No re-embedding needed

### 🎨 Notion-Style UI
- **Clean Sidebar** — API status, model selector, file info
- **Drag-and-Drop Upload** — Visual feedback during processing
- **Real-Time Chat** — Animated thinking indicator, smooth message rendering
- **Collapsible Citations** — Expand sources on demand

### 🔒 Privacy-First Architecture
- **Local Processing** — All chunking and embedding happens on-device
- **No Cloud Storage** — PDFs deleted after session
- **API Key Secured** — Stored in `.env`, never exposed to frontend
- **In-Memory Vectors** — Lost on server restart (no persistence without opt-in)

---

## 🛠️ Technology Stack

### Backend
| Component | Purpose | Library |
|---|---|---|
| **Web Framework** | REST API & routing | Flask 3.1.0 |
| **PDF Parsing** | Text extraction | pypdf 5.4.0 |
| **Document Processing** | DOCX, PPTX, images | python-docx, python-pptx, Pillow |
| **Embeddings** | Semantic search vectors | OpenRouter API (text-embedding-3-small) |
| **Vector Search** | Cosine similarity | NumPy 2.4.4 |
| **LLM Integration** | Chat completion | OpenAI SDK (OpenRouter-compatible) |
| **Environment** | Secrets management | python-dotenv |

### Frontend
- **Vanilla JavaScript** — Zero build step, pure DOM manipulation
- **Notion-Inspired CSS** — Light theme, clean typography
- **Responsive Design** — Works on desktop and tablet

### Infrastructure
- **Runtime** — Python 3.14+
- **Deployment** — Flask dev server (or Gunicorn for production)
- **API Provider** — OpenRouter (supports 100+ models)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.14+
- OpenRouter API key (free tier available)
- Internet connection

### Quick Start (60 seconds)
```bash
# 1. Clone the repo
git clone https://github.com/yourusername/studybuddy-rag.git
cd studybuddy-rag

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
# Edit .env and add your OpenRouter API key

# 5. Run the app
python app.py

# 6. Open browser
# http://localhost:5000
```

---

## 💡 Use Cases

### 📚 **Education & Learning**
- Students ask questions about textbooks, lecture notes, and research papers
- Professors prepare quiz materials from course PDFs
- Language learners get translations + explanations with source citations

### 📋 **Compliance & Audit**
- Legal teams search contracts for specific clauses
- Compliance officers extract regulatory requirements
- HR teams answer policy questions with accurate sources

### 💼 **Business & Research**
- Analysts summarize market research reports
- Teams extract key points from meeting transcripts
- Researchers cite exact locations in academic papers

### 🏥 **Healthcare & Documentation**
- Clinicians find evidence-based information in medical literature
- Patient coordinators answer common questions from documentation
- Researchers extract data from clinical trial reports

---

## 🎓 How RAG Works

```
1. UPLOAD → Extract text from any document
           ↓
2. CHUNK  → Split into 800-char overlapping pieces
           ↓
3. EMBED  → Convert chunks to semantic vectors (1536-dim)
           ↓
4. STORE  → Keep vectors in memory (session-based)
           ↓
5. QUERY  → User asks a question
           ↓
6. SEARCH → Embed question, find top-4 similar chunks
           ↓
7. CONTEXT → Build prompt with chunks + question
           ↓
8. LLM    → Send to language model (OpenRouter)
           ↓
9. CITE   → Return answer + source snippets
           ↓
10. DISPLAY → Show in chat with collapsible citations
```

---

## 📊 Performance

| Operation | Time | Notes |
|---|---|---|
| PDF upload (10 pages) | 2-5s | Text extraction + chunking |
| DOCX upload | 1-2s | Faster than PDF |
| Image upload | 3-8s | Includes GPT-4o Vision inference |
| Query response | 3-10s | Depends on model size (Llama 8B fastest) |
| Citation rendering | <1s | Pure client-side |

---

## 🔐 Security & Privacy

- ✅ **No tracking** — Queries not logged or stored
- ✅ **Encrypted secrets** — API keys in `.env` (gitignored)
- ✅ **No persistent DB** — Vectors deleted on session clear
- ✅ **Local processing** — Chunking/embedding on-device
- ✅ **Open source** — Full code transparency

---

## 📈 Roadmap

### Coming Soon
- [ ] Persistent vector database (ChromaDB, Weaviate)
- [ ] Multi-file sessions (upload 5+ PDFs at once)
- [ ] Conversation history & export as PDF
- [ ] User authentication & team workspaces
- [ ] Custom system prompts & RAG fine-tuning
- [ ] Batch processing API
- [ ] Docker containerization
- [ ] Kubernetes deployment templates

### Under Consideration
- [ ] Web UI file management
- [ ] Reranking (cross-encoder) for better relevance
- [ ] Hybrid search (BM25 + semantic)
- [ ] Streaming responses
- [ ] Mobile app (React Native)
- [ ] Browser extension

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to set up development environment
- Coding standards and style guide
- How to submit pull requests
- Bug report templates

---

## 📄 License

StudyBuddy RAG is released under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 💬 Support & Community

- **GitHub Issues** — [Report bugs](https://github.com/yourusername/studybuddy-rag/issues)
- **Discussions** — [Ask questions](https://github.com/yourusername/studybuddy-rag/discussions)
- **Email** — contact@studybuddy.dev
- **Twitter** — [@StudyBuddyRAG](https://twitter.com/studybuddyrag)

---

## 📚 Learn More

- [Architecture Overview](ARCHITECTURE.md) — How StudyBuddy works internally
- [API Documentation](API.md) — REST endpoint reference
- [Deployment Guide](DEPLOYMENT.md) — Run in production (Gunicorn, Docker, AWS)
- [Test Queries](TEST_QUERIES.md) — 12+ sample queries to validate functionality
- [Troubleshooting](TROUBLESHOOTING.md) — Common issues & solutions

---

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai) — Multi-model LLM access
- [PyPDF](https://github.com/py-pdf/pypdf) — PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) — DOCX/DOC parsing
- [python-pptx](https://python-pptx.readthedocs.io/) — PPTX parsing
- [Pillow](https://python-pillow.org/) — Image processing
- [NumPy](https://numpy.org/) — Efficient vector operations
- [Flask](https://flask.palletsprojects.com/) — Lightweight web framework

---

## ⭐ Show Your Support

If you find StudyBuddy RAG helpful, please:
- ⭐ **Star the repo** on GitHub
- 🐦 **Share on Twitter**
- 📢 **Tell your friends**
- 🐛 **Report bugs** to help us improve
- 💡 **Suggest features** in Discussions

---

**Built with ❤️ by the StudyBuddy team**

Last updated: May 2026
