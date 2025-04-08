import json
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.schema import Document

# -------- Settings --------
CHUNKS_PATH = Path("parsed/chunks.json")
FAISS_INDEX_DIR = "vectorstore"

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

# -------- Load Chunks --------
def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -------- Convert to LangChain Documents --------
def chunks_to_documents(chunks):
    return [
        Document(
            page_content=chunk["content"],
            metadata={
                "id": chunk["id"],
                "channel": chunk["channel"],
                "thread_title": chunk["thread_title"]
            }
        )
        for chunk in chunks
    ]

# -------- Main --------
def main():
    print("📄 Loading and converting chunks...")
    chunks = load_chunks()
    docs = chunks_to_documents(chunks)

    print("🔍 Creating embeddings...")
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    print("📦 Creating FAISS index...")
    vector_store = FAISS.from_documents(docs, embeddings)

    print(f"💾 Saving FAISS index to '{FAISS_INDEX_DIR}/'...")
    vector_store.save_local(FAISS_INDEX_DIR)

    print(f"✅ Done! {len(docs)} documents stored in FAISS.")

if __name__ == "__main__":
    main()
