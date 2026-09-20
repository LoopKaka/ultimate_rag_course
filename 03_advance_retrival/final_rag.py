from langchain_openai import ChatOpenAI
from config import TEXT_MODEL
from final_retrieval import retrive_chunks
from filter_config import create_metadata_config
from reranker import rerank_document

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

def generate_llm_answer(question, topic):
    # Create Filter
    fiter_config = create_metadata_config(topic)
    # Get 20 relevent chunks
    relevent_chunks = retrive_chunks(question, top_k=20, metadata_filter_config=fiter_config)
    # Reranking
    most_relevent_chunks = rerank_document(question, relevent_chunks, 5)
    # COnvert to text
    context = format_chunks(most_relevent_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    # Get answer from LLM
    result = llm.invoke(prompt)

    return result.content

if __name__ == "__main__":
    while True:
        question = input("\nUser: ")
        if question.lower() == "exit":
            break

        topic = input("Topic (Press Enter for all): ")

        answer = generate_llm_answer(question, topic)
        print("Answer: ", answer)
