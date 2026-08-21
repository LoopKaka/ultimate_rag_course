from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# from qdrant_client import QdrantClient, models

# DB_URL = "http://localhost:6333/"

# client = QdrantClient(
#     url=DB_URL
# )

# client.create_collection(
#     collection_name="Test",
#     vectors_config=models.VectorParams(
#         size=3,
#         distance=models.Distance.COSINE
#     )
# )

# client.upsert(
#     collection_name="Test",
#     points=[
#         models.PointStruct(
#             id=1,
#             vector=[0.1,0.2,0.3],
#             payload={
#                 "text": "Next js is a react farmework.",
#                 "source": "some.md",
#                 "page_no": 1
#             }
#         )
#     ]
# )

# print(client.get_collections())

load_dotenv()

DOCUMENT_PATH = "./datasource_documents"
DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "tech_documents"

def load_documents():
    loader = DirectoryLoader(
        DOCUMENT_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()

    print("No of Documents: ", len(documents))

    return documents

def chunking_document(documents):
    text_spliter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return text_spliter.split_documents(documents=documents)

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def strore_in_db(chunks):
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding,
        url=DB_URL,
        collection_name=COLLECTION_NAME
    )

    print("Stored in Database")

documents = load_documents()
chunks = chunking_document(documents)
print("Documents: ", len(documents))
print("Chunks: ", len(chunks))

strore_in_db(chunks)