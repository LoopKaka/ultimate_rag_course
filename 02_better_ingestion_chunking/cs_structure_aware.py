from langchain_text_splitters import (MarkdownHeaderTextSplitter)
from document_loader import (load_md_documents)

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

documents = load_md_documents()
chunks = splitter.split_text(documents[0].page_content)

for index, chunk in enumerate(chunks):
    print("="*80)
    print(f"Chunk No: {index+1}")
    print("-"*80)

    print("Metadata: ", chunk.metadata, "\n")
    print("Content: ", chunk.page_content, "\n")