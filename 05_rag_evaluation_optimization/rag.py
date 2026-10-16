from langchain_openai import ChatOpenAI
from config import TEXT_MODEL
from retrieval import retrive_chunks

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

def format_chunks(documents):
    context = ""
    for index, (document, score) in enumerate(documents):
        context += (
            f"Document {index+1}\n"
            f"{document.page_content}\n\n"
        )
    return context

def get_chunk_ids(documents):
    retrieved_chunk_ids = []

    for document, _ in documents:
        chunk_id = document.metadata.get("chunk_id")
        retrieved_chunk_ids.append(chunk_id)

    return retrieved_chunk_ids



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

def generate_llm_answer(question, top_k):
    documents = retrive_chunks(question, top_k)
    context = format_chunks(documents)
    retrieved_chunk_ids = get_chunk_ids(documents)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    result = llm.invoke(prompt)

    return {
        "answer": result.content,
        "context": context,
        "retrieved_chunk_ids": retrieved_chunk_ids
    }

