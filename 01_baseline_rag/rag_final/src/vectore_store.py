from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from rag_final.src.config import (COLLECTION_NAME, DB_URL, EMBEDDING_MODEL)

embedding = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

def create_vectore_store(chunks):
    return QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedding,
            url=DB_URL,
            collection_name=COLLECTION_NAME
        )

def get_vector_store():
    return QdrantVectorStore.from_existing_collection(
        collection_name=COLLECTION_NAME,
        url=DB_URL,
        embedding=embedding
    )