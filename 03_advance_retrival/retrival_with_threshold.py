from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

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

def retrive_chunks(query, top_k=5, score_threshold=0.7):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
        score_threshold=score_threshold
    )

    return results


if __name__ == "__main__":
    question = input("User: ")
    relevent_chunks = retrive_chunks(question)

    for index, (document, score) in enumerate(relevent_chunks):
        print("="*80)
        print("Chunk No: ", index+1)
        print("Score: ", score)
        print("-"*80)

        print("Content:", document.page_content, "\n")
        print("Metadata:", document.metadata, "\n")