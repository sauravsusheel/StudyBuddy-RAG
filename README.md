# 🛡️ SecurAudit RAG

An enterprise-grade **Corporate IT Security & Compliance Auditor** that audits vendor policy texts against authoritative compliance frameworks (NIST, ISO, GDPR, and internal IT policies) using Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- **Reference Framework Ingestion** — Drag & drop any authoritative compliance standard (PDF, Word, or presentation) to build the reference database.
- **Systematic Vendor Auditing** — Paste vendor security policies, terms of service, or DPAs to run a rigorous gap analysis.
- **Consolidated RAG Pipeline** — Chunks vendor text, retrieves the most relevant corporate rules for each chunk, and aggregates context.
- **Strict Auditor Prompting** — Enforces deterministic reasoning (temp = 0.0), absolute compliance with retrieved facts (no hallucinations), and structured markdown reporting.
- **Interactive compliance Q&A** — Switch to the "Interactive Chat" tab to ask ad-hoc questions about your uploaded guidelines.
- **Modern Security Dashboard UI** — A premium, dark-slate visual style replacing default browser aesthetics.

---

## 🗂 Project Structure

```
SecurAudit RAG/
├── app.py              # Flask backend — RAG engine & Auditor pipeline
├── requirements.txt    # Python dependencies
├── start.bat           # Windows startup script
├── uploads/            # Temporary document storage (auto-deleted on session reset)
├── vectorstores/       # Reserved for future persistence
└── static/
    ├── index.html      # Security Dashboard layout (Tabbed Interface)
    ├── style.css       # Sleek Slate-Dark theme & badge definitions
    └── app.js          # Tabs management, audit trigger, & custom markdown parser
```

---

## ⚙️ How It Works

```
1. Ingest Corporate Framework
   └─ Upload NIST, ISO, GDPR, or Internal Policy document
   └─ Text split into 800-char chunks and embedded via text-embedding-3-small
   └─ Embeddings saved in-memory as a normalized numpy array

2. Paste Vendor Policy (Audit Mode)
   └─ Click "Run Compliance Audit"
   └─ Vendor text split into paragraphs/sentences
   └─ Each paragraph embedded and matched against corporate framework embeddings
   └─ Top matches compiled into "RETRIEVED COMPLIANCE CONTEXT"
   └─ LLM queried with a deterministic system prompt (temp 0.0)

3. Generate Audit Report
   └─ Enforces structured markdown schema
   └─ Output includes: Verdict (APPROVED / CONDITIONAL PASS / FLAGGED & REJECTED)
   └─ Output lists exact policy violations with [Doc: Name, Page: X] citations
   └─ Displays a concise Data Transparency & Evidence table in the UI
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- An OpenRouter API key configured in `.env` (copied from `.env.example`)

### Run the app

**Option 1 — Double-click:**
```
start.bat
```

**Option 2 — Terminal:**
```bash
.\venv\Scripts\python.exe app.py
```

Then open **http://localhost:5000** in your browser.

---

## 🔑 API Key

Create a `.env` file in the root directory:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```
*(Get your key at [openrouter.ai](https://openrouter.ai))*

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework & API routing |
| `flask-cors` | Cross-Origin Resource Sharing |
| `pypdf` | PDF parsing & text extraction |
| `openai` | API communication with OpenRouter |
| `numpy` | High-speed vector dot-product calculations |
| `python-dotenv` | Loads environment variables from `.env` |
| `python-docx` | Word document text extraction |
| `python-pptx` | PowerPoint presentation parsing |
| `pillow` | Image loading & resizing for OCR |

---

## 💡 Audit Verdict Types

- <span style="color:#10b981;font-weight:bold;">APPROVED</span> — Vendor policies align completely with the authoritative compliance frameworks.
- <span style="color:#f59e0b;font-weight:bold;">CONDITIONAL PASS</span> — Minor deviations detected, remediations recommended.
- <span style="color:#ef4444;font-weight:bold;">FLAGGED & REJECTED</span> — Critical compliance conflicts found (e.g. data retention violations, weak authentication standards).
