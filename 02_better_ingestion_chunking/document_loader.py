from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    BSHTMLLoader,
    DirectoryLoader
)

DOCUMENTS_PATH = "mix_documents"

def load_pdf_documents():
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )

    return loader.load()

def load_text_documents():
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )

    return loader.load()

def load_md_documents():
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )

    return loader.load()

def load_html_documents():
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.html",
        loader_cls=BSHTMLLoader,
        show_progress=True
    )

    return loader.load()

def load_docx_documents():
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.docx",
        loader_cls=Docx2txtLoader,
        show_progress=True
    )

    return loader.load()

def load_documents():
    documents = []
    
    documents.extend(
        load_pdf_documents()
    )

    documents.extend(
        load_text_documents()
    )

    documents.extend(
        load_md_documents()
    )

    documents.extend(
        load_html_documents()
    )

    documents.extend(
        load_docx_documents()
    )

    return documents


if __name__ == "__main__":
    documents = load_documents()
    print("No of documents: ", len(documents), "\n")
    for index, document in enumerate(documents):
        print("="*80)
        print(f"Document No.: {index+1}")
        print("-"*80)

        print("Source: ", document.metadata.get("source"), "\n")
        print("Metadata: ", document.metadata, "\n")
        print("Page Content: ", document.page_content, "\n")