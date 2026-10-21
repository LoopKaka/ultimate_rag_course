from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from config import TEXT_MODEL

class QueryRewritterResp(BaseModel):
    search_query: str = None

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

structured_llm = llm.with_structured_output(
    QueryRewritterResp
)

PROMPT_TEMPLATE = """
You rewrite search queries for a technical documentation RAG system.

Create a better search query that helps retrieve evidence for the
user's original question.

Rules:
- Preserve the user's original intent.
- Do not answer the question.
- Return only the rewritten search query.
- Use clear technical terms and relevant synonyms.
- Do not introduce unrelated topics.
- Make the query meaningfully different from the previous search query
  when possible.

Orginal user question:
{question}

Previous Search question:
{search_query}

Rewrite the search query to improve retrieval.
"""

def query_rewritter(question, previous_question):
    prompt = PROMPT_TEMPLATE.format(
        question=question, search_query=previous_question
    )

    result = structured_llm.invoke(prompt)

    return result.search_query

