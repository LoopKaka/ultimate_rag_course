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

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "fetch_k": 20, # First consider 20 candidate documents
        "k": 5, # Finally select 5 documents.
        "lambda_mult": 0.5 # 1 - More emphasis on relevance, 0 - More emphasis on diversity
    }
)

if __name__ == "__main__":
    user_input = input("User: ")

    documents = retriever.invoke(user_input)

    for index, document in enumerate(documents):
        print("="*80)
        print("Document#", index+1)
        print("-"*80)

        print(document.page_content, "\n")
        print(document.metadata, "\n")