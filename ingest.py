import os
import re
import chromadb
from pathlib import Path
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "your-openrouter-api-key-here")
OPENROUTER_BASE = "https://openrouter.ai/api/v1"
EMBED_MODEL     = "text-embedding-3-small"

COMPLIANCE_CORPUS = Path("compliance_corpus")
COMPLIANCE_CORPUS.mkdir(exist_ok=True)
CHROMA_DB = Path("chroma_db")
CHROMA_DB.mkdir(exist_ok=True)

def clean_text(text: str) -> str:
    # Remove redundant whitespaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def main():
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print("[ERROR] Please configure your OPENROUTER_API_KEY in .env")
        return

    # Initialize OpenRouter / OpenAI client
    client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE)

    # Initialize Chroma client
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB))
    collection = chroma_client.get_or_create_collection("compliance_frameworks")

    print("=== SecurAudit RAG: Batch Ingestion ===")
    
    pdf_files = list(COMPLIANCE_CORPUS.glob("*.pdf"))
    if not pdf_files:
        print(f"[WARN] No PDF files found in {COMPLIANCE_CORPUS.resolve()}")
        print("Please place your compliance framework PDFs (e.g. NIST, ISO, GDPR, HIPAA) there and re-run.")
        return

    total_chunks = 0
    for pdf_path in pdf_files:
        filename = pdf_path.name
        doc_name_clean = pdf_path.stem.replace("_", " ").replace("-", " ").upper()
        print(f"\nProcessing '{filename}' ({doc_name_clean})...")
        
        # Check if already indexed in ChromaDB
        try:
            existing = collection.get(where={"document_id": filename}, limit=1)
            if existing and existing["ids"]:
                print(f"  '{filename}' is already indexed. Skipping.")
                continue
        except Exception as e:
            print(f"  [WARN] Error checking index status for {filename}: {e}")

        try:
            reader = PdfReader(str(pdf_path))
            pages_data = []
            
            # Extract and chunk page by page
            for page_idx, page in enumerate(reader.pages):
                raw_text = page.extract_text()
                if not raw_text:
                    continue
                
                cleaned = clean_text(raw_text)
                if not cleaned:
                    continue
                
                page_chunks = chunk_text(cleaned)
                for chunk in page_chunks:
                    pages_data.append({
                        "text": chunk,
                        "page": page_idx + 1 # 1-based page numbering
                    })

            if not pages_data:
                print(f"  [WARN] No text extracted from {filename}.")
                continue

            print(f"  Extracted {len(pages_data)} chunks. Generating embeddings...")

            # Batch embed and store
            batch_size = 512
            for i in range(0, len(pages_data), batch_size):
                batch = pages_data[i : i + batch_size]
                texts = [b["text"] for b in batch]
                
                # Fetch embeddings from OpenRouter
                resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
                embeddings = [item.embedding for item in sorted(resp.data, key=lambda x: x.index)]
                
                ids = [f"{filename}_p{b['page']}_c{idx + i}" for idx, b in enumerate(batch)]
                metadatas = [{
                    "document_id": filename,
                    "doc_name_clean": doc_name_clean,
                    "page_number": b["page"]
                } for b in batch]

                # Add to ChromaDB
                collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas
                )
                
            total_chunks += len(pages_data)
            print(f"  Successfully indexed {filename} ({len(pages_data)} chunks added).")

        except Exception as e:
            print(f"  [ERROR] Failed to process {filename}: {str(e)}")

    print(f"\n=== Ingestion Complete. Total chunks indexed: {total_chunks} ===")

if __name__ == "__main__":
    main()
