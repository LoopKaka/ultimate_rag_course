from typing import Literal, TypedDict

from langgraph.graph import START, END, StateGraph
from retrieval import retrive_chunks
from generation import generate_llm_answer
from grading import check_grading
from config import TOP_K

class State(TypedDict):
    question: str
    context: str
    answer: str
    is_relevent: bool

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

def grading_node(state: State) -> dict:
    print("Grading...")
    
    question = state["question"]
    context = state["context"]
    is_relevent = check_grading(question, context)

    return {
        "is_relevent": is_relevent
    }

def fallback_node(state: State) -> dict:
    print("Fallback...")

    return {
        "answer": "I couldn't find this information in the knowledge base."
    }

# Conditional Node
def route_after_grading(state: State) -> Literal["generation", "fallback"]:
    print("Routing...")

    if state["is_relevent"]:
        return "generation"
    return "fallback"
    

# Graph Builder
builder = StateGraph(State)

# Register Nodes
builder.add_node("retrieval", retrieval_node)
builder.add_node("generation", generation_node)
builder.add_node("grading", grading_node)
builder.add_node("fallback", fallback_node)

# Connect Edges
builder.add_edge(START, "retrieval")
builder.add_edge("retrieval", "grading")
builder.add_conditional_edges("grading", route_after_grading, {
    "generation": "generation",
    "fallback": "fallback"
})
builder.add_edge("generation", END)
builder.add_edge("fallback", END)

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