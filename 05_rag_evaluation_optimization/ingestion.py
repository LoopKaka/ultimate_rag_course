from collections import defaultdict
from pathlib import Path
import uuid

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import (
    QdrantVectorStore, FastEmbedSparse, RetrievalMode
)

load_dotenv()

DOCUMENT_PATH = "./evaluation_documents"
DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "rag_evaluation"

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
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return text_spliter.split_documents(documents=documents)

dense_embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

sparse_embedding = FastEmbedSparse(
    model="Qdrant/bm25"
)

def strore_in_db(chunks):
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=dense_embedding,
        sparse_embedding=sparse_embedding,
        url=DB_URL,
        collection_name=COLLECTION_NAME,
        retrieval_mode=RetrievalMode.HYBRID
    )

    print("Stored in Database")

def enrich_document_metadata(document):
    source = Path(document.metadata.get("source", ""))

    try:
        relevent_source = source.relative_to(DOCUMENT_PATH).as_posix()
    except ValueError:
        relevent_source = source.as_posix()

    document.metadata["document_id"] = (
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            relevent_source
        )
    )
    document.metadata["file_name"] = (source.name)
    document.metadata["file_type"] = (source.suffix.lower().replace(".", ""))
    document.metadata["topic"] = (source.stem)

    return document

def enrich_chunk_metadata(chunks):
    counter = defaultdict(int)

    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        chunk_index = counter[source]

        chunk.metadata["chunk_index"] = (chunk_index)
        chunk.metadata["chunk_id"] = (
            f"{source}::chunk-{chunk_index}"
        )
        counter[source] += 1
    return chunks

documents = load_documents()
for document in documents:
    enrich_document_metadata(document)

chunks = chunking_document(documents)
chunks_with_metadata = enrich_chunk_metadata(chunks)
print("Documents: ", len(documents))
print("Chunks: ", len(chunks))

strore_in_db(chunks_with_metadata)