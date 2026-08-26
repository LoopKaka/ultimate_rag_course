from rag_final.src.ingestion import load_doc_and_chunk
from rag_final.src.vectore_store import create_vectore_store

def main():
    print("Ingestion Is Inprogress")
    chunks = load_doc_and_chunk()
    create_vectore_store(chunks)
    print("Ingestion Completed")


if __name__ == "__main__":
    main()