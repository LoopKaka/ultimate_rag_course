from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from config import TEXT_MODEL
from langchain_core.documents import Document

load_dotenv()

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

PROMPT = """
You are a context compression component for a technical RAG system.

User question:
{query}

Document:
{document_page_content}

Extract only the information from the document
that is directly relevant to answering the user's
question.

Rules:
- Do not add information.
- Do not answer the question.
- Preserve important technical details.
- Remove irrelevant information.
- If the document contains no relevant information,
  return an empty string.

  
Return only the relevant content.
"""

def compression(query, document):
    prompt = PROMPT.format(
        query=query, document_page_content=document.page_content
    )

    response = llm.invoke(prompt)

    return Document(
        page_content=response.content,
        metadata=document.metadata
    )



    