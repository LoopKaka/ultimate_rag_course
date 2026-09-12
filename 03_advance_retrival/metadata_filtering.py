# from qdrant_client.models import Filter, FieldCondition, MatchValue
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from filter_config import create_metadata_config

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

# filter_metadata = Filter(
#     must=[
#         FieldCondition(
#             key="metadata.topic",
#             match=MatchValue(
#                 value="springboot"
#             )
#         )
#     ]
# )

def retrive_chunks(query, top_k=5, filter_metadata=None):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
        filter=filter_metadata
    )

    return results


if __name__ == "__main__":
    question = input("User: ")
    topic = input("Topic (Press Enter for all): ")
    filter_metadata = create_metadata_config(topic=topic)
    relevent_chunks = retrive_chunks(
        question, filter_metadata=filter_metadata
    )

    for index, (document, score) in enumerate(relevent_chunks):
        print("="*80)
        print("Chunk No: ", index+1)
        print("Score: ", score)
        print("-"*80)

        print("Content:", document.page_content, "\n")
        print("Metadata:", document.metadata, "\n")