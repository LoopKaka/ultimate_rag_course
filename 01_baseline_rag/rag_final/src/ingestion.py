from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter

DOCUMENT_PATH = "../datasource_documents"

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

def load_doc_and_chunk():
    documents = load_documents()
    return chunking_document(documents)