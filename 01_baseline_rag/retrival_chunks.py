# from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

"""
load_dotenv()

DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "tech_documents"

client = QdrantClient(
    url=DB_URL
)

user_query = "What is springboot?"

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

query_vector = embedding.embed_query(user_query)

print("Query Vector: ", query_vector[:3])

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=1,
    with_payload=False
)

for result in results.points:
    print("="*80)
    print("Score: ", result.score)
    print("Payload: ", result.payload)

"""

load_dotenv()

DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "tech_documents"

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=DB_URL,
    embedding=embedding
)

def retrive_chunks(query, top_k=5):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return results


user_query = input("User Query > ")
results = retrive_chunks(user_query)

for index, (document, score) in enumerate(results):
    print("="*80)
    print("Chunk No: ", index+1)
    print("Score: ", score)

    print("\nContent: \n", document.page_content)
    print("Metadata: \n", document.metadata)