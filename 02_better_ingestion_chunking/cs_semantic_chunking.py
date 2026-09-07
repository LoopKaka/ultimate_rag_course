from langchain_experimental.text_splitter import (SemanticChunker)
from document_loader import (load_documents)
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

splitter = SemanticChunker(embeddings)

documents = load_documents()
chunks = splitter.split_documents(documents)

for index, chunk in enumerate(chunks):
    print("="*80)
    print(f"Chunk No: {index+1}")
    print("-"*80)

    print("Metadata: ", chunk.metadata, "\n")
    print("Content: ", chunk.page_content, "\n")