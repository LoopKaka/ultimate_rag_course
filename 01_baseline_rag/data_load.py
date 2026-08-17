from langchain_community.document_loaders import DirectoryLoader, TextLoader

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
    
documents = load_documents()

for document in documents:
    print("================== \n")
    print("Page Content: ", document.page_content, "\n")
    print("Metadata: ", document.metadata, "\n")