from langchain_openai import ChatOpenAI
from rag_final.src.vectore_store import (get_vector_store)
from rag_final.src.config import (TEXT_MODEL, TOP_K)

vector_store = get_vector_store()

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

def retrive_chunks(query, top_k=TOP_K):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return results

def format_chunks(documents):
    context = ""
    for index, (document, score) in enumerate(documents):
        context += (
            f"Document {index+1}\n"
            f"{document.page_content}\n\n"
        )
    return context

PROMPT_TEMPLATE = """
You are a helpful AI assistant.
Answer the user's question ONLY using the provided context.

If the answer cannot be found in the context,
say: "I couldn't find this information in the knowledge base."

Do not make up assumptions.

Context
-----------
{context}
-----------

Question:
{question}

Answer:
"""

def generate_llm_answer(question):
    documents = retrive_chunks(question)
    context = format_chunks(documents)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    result = llm.invoke(prompt)

    return result.content