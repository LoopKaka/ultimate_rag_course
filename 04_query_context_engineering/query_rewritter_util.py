from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

POMPT_FOR_ANALYSE_REWRITE="""
You are a query analysis and rewriting component 
for a technical documentation RAG system.
Your job is to determine whether the user's latest question needs rewriting 
before retrieval.

A query needs rewriting when:
- It depends on previous conversation context.
- It contains ambiguous references such as
  "it", "this", "that", "they", or "its".
- Important context is missing.
- Rewriting would make the retrieval intent clearer.

A query does NOT need rewriting when:
- It is already clear and standalone.
- It contains the necessary technical terms.
- It can be directly used for retrieval.

If rewriting is NOT needed:
- Keep the original query unchanged.

If rewriting IS needed:
- Rewrite it into a concise standalone search query.
- Preserve the original intent.
- Include important technical terms from the conversation.

Return ONLY valid JSON:

{{
    "rewrite": true or false,
    "search_query": "..."
}}

Conversation History:
{conversation_history}

User New Question:
{question}
"""

PROMPT = """
You are a query rewriting component for a technical documentation RAG system.
Your job is to convert the user's latest question into a clear, standalone 
search query.

Rules:
1. Preserve the user's original intent.
2. Use conversation history to resolve ambiguous references such as "it", 
"this", and "that".
3. Include important technical terms from the conversation when necessary.
4. Keep the query concise.
5. Do not answer the question.
6. Return only the rewritten search query.

Conversation History:
{conversation_history}

User New Question:
{question}
"""

def conversation_formatting(conversation_history=[]):
    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation_history
    )

    return conversation_text


def query_analyser_rewritter(query=None, conversation_history=None):
    prompt = POMPT_FOR_ANALYSE_REWRITE.format(question=query, 
                        conversation_history=conversation_history)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip()

def query_rewritter(query=None, conversation_history=None):
    prompt = PROMPT.format(question=query, conversation_history=conversation_history)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip()

"""
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break

        convesation_history = [
            {"role": "user", "content": "What is expressjs?"},
            {"role": "assistant", "content": "What is Express.js in web development?"},
        ]
        new_query = query_analyser_rewritter(
            user_input, conversation_formatting(convesation_history)
            )
        print(new_query)

"""
