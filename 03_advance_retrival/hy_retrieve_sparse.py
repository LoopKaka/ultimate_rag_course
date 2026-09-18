from langchain_qdrant import (
    QdrantVectorStore, FastEmbedSparse, RetrievalMode
)
from dotenv import load_dotenv

load_dotenv()

DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "hybrid_tech_documents"

sparse_embedding = FastEmbedSparse(
    model="Qdrant/bm25"
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=DB_URL,
    sparse_embedding=sparse_embedding,
    retrieval_mode=RetrievalMode.SPARSE
)

def sparse_retrive_chunks(query, top_k=5):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return results


if __name__ == "__main__":
    question = input("User: ")
    relevent_chunks = sparse_retrive_chunks(question)

    for index, (document, score) in enumerate(relevent_chunks):
        print("="*80)
        print("Chunk No: ", index+1)
        print("Score: ", score)
        print("-"*80)

        print("Content:", document.page_content, "\n")
        print("Metadata:", document.metadata, "\n")