from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

DB_URL = "http://localhost:6333/"
COLLECTION_NAME = "tech_documents"

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=DB_URL,
    embedding=embedding
)

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

def retrive_chunks(query, top_k=5):
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


while True:
    question = input("You: ")

    if question.lower() == 'exit':
        break

    answer = generate_llm_answer(question)
    print("Answer: ", answer)