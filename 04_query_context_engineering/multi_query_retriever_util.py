from typing import List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from config import TEXT_MODEL
from pydantic import BaseModel
from retriever import retrive_chunks
from reranking import rerank_document
from context_selection import select_context
from context_compression import compression

load_dotenv()

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

class QuestionResponse(BaseModel):
    questions: List[str]

structured_llm = llm.with_structured_output(
    QuestionResponse
)

PROMPT = """
You are helping a technical documentation RAG system improve retrieval.
Generate {number_of_queries} different search queries for the user's question.

Rules:
1. Preserve the original information need.
2. Each query should approach the question from a slightly different perspective.
3. Include important technical terms.
4. Keep each query concise.
5. Do not answer the user's question.
6. Do not add explanations.
7. Do not use Markdown.
8. Do not use code fences.
9. Return ONLY valid JSON.
10. The JSON must contain exactly one key: "questions".
11. The value of "questions" must be an array of strings.
12. Generate exactly {number_of_queries} strings in the array.

Required JSON structure:
{{
    "questions": [
        "question 1",
        "question 2",
        "question 3"
    ]
}}

User Question:
{query}
"""

def generate_multiple_queries(query=None, number_of_queries=3):
    prompt = PROMPT.format(query=query, number_of_queries=number_of_queries)
    response = structured_llm.invoke(prompt)
    return response.questions

def retrive_multi_query(queries):
    merge_chunks = []
    for query in queries:
        relevent_chunks = retrive_chunks(query)
        merge_chunks.extend(relevent_chunks)
    return merge_chunks

def remove_duplicate_chunks(relevent_chunks):
    unique_chunks = []
    seen = set()

    for document, score in relevent_chunks:
        source = document.metadata.get("source", "")
        chunk_index = document.metadata.get("chunk_index", "")

        # You need insert chunk index during ingestion of the document in Qdrant DB
        key = (source, chunk_index)

        if key in seen:
            continue

        seen.add(key)
        unique_chunks.append((document, score))

    return unique_chunks


def multi_query_retriever(user_input, query, number_of_queries=3):
    queries = generate_multiple_queries(query, number_of_queries)
    relevent_chunks = retrive_multi_query(queries)
    unique_chunks = remove_duplicate_chunks(relevent_chunks)
    top_chunks = rerank_document(user_input, unique_chunks, top_k=20)

    # Episode for context selection
    # selected_chunks = select_context(top_chunks, top_k=5, score_threshold=0.1)
    # return selected_chunks

    # Episode for context compression
    # compressed_docs = []
    # for document, score in selected_chunks:
    #     compressed_doc = compression(query=query, document=document)
    #     print("Compressed Doc >> ", compressed_doc, "\n")
    #     compressed_docs.append((compressed_doc, score))

    return top_chunks

"""
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break

        queries = generate_multiple_queries(user_input)
        relevent_chunks = retrive_multi_query(queries)
        unique_chunks = remove_duplicate_chunks(relevent_chunks)
        print(unique_chunks)
"""
