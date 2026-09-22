from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse
from dotenv import load_dotenv

load_dotenv()

DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "hybrid_tech_documents"

dense_embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

sparse_embedding = FastEmbedSparse(
    model="Qdrant/bm25"
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=DB_URL,
    embedding=dense_embedding,
    sparse_embedding=sparse_embedding
)

def retrive_chunks(query, top_k=5):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return results
