from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

from config import (
    DB_URL, COLLECTION_NAME, BM25_EMBEDDING_MODEL, EMBEDDING_MODEL, TOP_K,
    SCORE_THRESHOLD
)

dense_embedding = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

sparse_embedding = FastEmbedSparse(
    model=BM25_EMBEDDING_MODEL
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=DB_URL,
    embedding=dense_embedding,
    sparse_embedding=sparse_embedding,
    retrieval_mode=RetrievalMode.HYBRID
)

def retrive_chunks(query, top_k=TOP_K, metadata_filter_config=None ):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
        filter=metadata_filter_config,
        score_threshold=SCORE_THRESHOLD
    )

    return results