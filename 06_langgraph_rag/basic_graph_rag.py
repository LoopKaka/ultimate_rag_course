from typing import TypedDict

from langgraph.graph import START, END, StateGraph
from retrieval import retrive_chunks
from generation import generate_llm_answer
from config import TOP_K

class State(TypedDict):
    question: str
    context: str
    answer: str

def retrieval_node(state: State) -> dict:
    print("Rertival is in progress...")

    question = state["question"]
    context = retrive_chunks(question, TOP_K)

    return {
        "context": context
    }

def generation_node(state: State) -> dict:
    print("Generation is in progress...")

    question = state["question"]
    context = state["context"]
    answer = generate_llm_answer(question, context)

    return {
        "answer": answer
    }

# Graph Builder
builder = StateGraph(State)

# Register Nodes
builder.add_node("retrieval", retrieval_node)
builder.add_node("generation", generation_node)

# Connect Edges
builder.add_edge(START, "retrieval")
builder.add_edge("retrieval", "generation")
builder.add_edge("generation", END)

graph = builder.compile()

if __name__ == "__main__":
    user_input = input("User > ")
    state = {
        "question": user_input,
        "context": "",
        "answer": ""
    }

    result = graph.invoke(state)

    print("Answer > ", result["answer"])