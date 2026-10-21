from langchain_openai import ChatOpenAI
from config import TEXT_MODEL

llm = ChatOpenAI(
    model=TEXT_MODEL,
    temperature=0
)

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

def generate_llm_answer(question, context):
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    result = llm.invoke(prompt)

    return result.content

