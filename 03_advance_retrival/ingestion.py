from pathlib import Path
import uuid

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

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

def enrich_document_metadata(document):
    source = document.metadata.get("source", "")

    path = Path(source)

    document.metadata["file_name"] = (path.name)
    document.metadata["file_type"] = (path.suffix.lower().replace(".", ""))
    document.metadata["document_id"] = uuid.uuid4()
    document.metadata["topic"] = (path.name.removesuffix(".md"))

    return document

documents = load_documents()
for document in documents:
    enrich_document_metadata(document)

chunks = chunking_document(documents)
print("Documents: ", len(documents))
print("Chunks: ", len(chunks))

strore_in_db(chunks)