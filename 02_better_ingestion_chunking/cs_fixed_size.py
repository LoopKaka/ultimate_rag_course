from langchain_text_splitters import (CharacterTextSplitter)
from document_loader import (load_documents)

splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

documents = load_documents()
chunks = splitter.split_documents(documents)

for index, chunk in enumerate(chunks):
    print("="*80)
    print(f"Chunk No: {index+1}")
    print("-"*80)

    print("Metadata: ", chunk.metadata, "\n")
    print("Content: ", chunk.page_content, "\n")