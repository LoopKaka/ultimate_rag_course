from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()
# For Simple embed_query
# embedding = OpenAIEmbeddings(
#     model="text-embedding-3-small"
# )

# text = "Next.js is a react farmework"

# vector = embedding.embed_query(text)

# print("Length: ", len(vector))
# print("First 3 values: ", vector[:3])

DOCUMENT_PATH = "./datasource_documents"

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
def generate_embeddings(chunks):
    vectors = embedding.embed_documents(
       [chunk.page_content for chunk in chunks] 
    )

    return vectors

documents = load_documents()
chunks = chunking_document(documents)
vectors = generate_embeddings(chunks)

print("Documents: ", len(documents))
print("Chunks: ", len(chunks))
print("Vectors generated: ", len(vectors))