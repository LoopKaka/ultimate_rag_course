from document_loader import load_documents
from metadata import (enrich_document_metadata, enrich_chunk_metadata)
from langchain_text_splitters import CharacterTextSplitter

def chunking_document(documents):
    text_spliter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return text_spliter.split_documents(documents=documents)

def main():
    documents = load_documents()
    for document in documents:
        enrich_document_metadata(document)

    chunks = chunking_document(documents)

    enrich_chunk_metadata(chunks)

    return chunks

if __name__ == "__main__":
    chunks = main()

    for index, chunk in enumerate(chunks):
        print("="*80)
        print(f"Chunk No: {index+1}")
        print("-"*80)

        print("Metadata: ", chunk.metadata, "\n")
        print("Content: ", chunk.page_content, "\n")


