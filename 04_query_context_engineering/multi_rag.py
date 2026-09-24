from langchain_openai import ChatOpenAI
from config import TEXT_MODEL
from retriever import retrive_chunks
from query_rewritter_util import query_analyser_rewritter
from multi_query_retriever_util import multi_query_retriever

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

def generate_llm_answer(user_input, question):
    ## Multi query retrival
    top_chunks = multi_query_retriever(user_input, question)
    context = format_chunks(top_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    result = llm.invoke(prompt)

    return result.content

if __name__ == "__main__":
    conversation_history = []
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break

        new_query = query_analyser_rewritter(user_input, conversation_history)
        answer = generate_llm_answer(user_input, new_query)
        print("LLM: ", answer)

        # Save conversation
        conversation_history.append(
            {"role": "user", "content": user_input}
        )

        conversation_history.append(
            {"role": "assistant", "content": new_query}
        )

