from langchain_text_splitters import (RecursiveCharacterTextSplitter)
from document_loader import (load_documents)

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=300,
    chunk_overlap=30,
)

documents = load_documents()
chunks = splitter.split_text(documents)

for index, chunk in enumerate(chunks):
    print("="*80)
    print(f"Chunk No: {index+1}")
    print("-"*80)

    print("Metadata: ", chunk.metadata, "\n")
    print("Content: ", chunk.page_content, "\n")