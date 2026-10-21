from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import (
    QdrantVectorStore, FastEmbedSparse, RetrievalMode
)
from dotenv import load_dotenv
from config import (
    DB_URL, EVALUATE_RAG_COLLECTION, EMBEDDING_MODEL, BM25_EMBEDDING_MODEL
)

load_dotenv()

dense_embedding = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

sparse_embedding = FastEmbedSparse(
    model=BM25_EMBEDDING_MODEL
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=EVALUATE_RAG_COLLECTION,
    url=DB_URL,
    embedding=dense_embedding,
    sparse_embedding=sparse_embedding,
    retrieval_mode=RetrievalMode.HYBRID
)

def format_chunks(documents):
    context = ""
    for index, (document, score) in enumerate(documents):
        context += (
            f"Document {index+1}\n"
            f"{document.page_content}\n\n"
        )
    return context

def retrive_chunks(query, top_k=5):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return format_chunks(results)