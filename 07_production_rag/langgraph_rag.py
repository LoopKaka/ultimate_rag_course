from typing import Literal, TypedDict

from langgraph.graph import START, END, StateGraph
from retrieval import retrive_chunks
from generation import generate_llm_answer
from grading import check_grading
from query_rewrting import query_rewritter
from config import TOP_K, MAX_RETRY_LIMIT

class State(TypedDict):
    question: str
    context: str
    answer: str
    is_relevent: bool
    retry_count: int
    search_query: str

def retrieval_node(state: State) -> dict:
    print("Rertival is in progress...")

    question = state["search_query"]
    context = retrive_chunks(question, TOP_K)

    return {
        "context": context
    }

def generation_node(state: State) -> dict:
    print("Generation is in progress...")

    question = state["search_query"]
    context = state["context"]
    answer = generate_llm_answer(question, context)

    return {
        "answer": answer
    }

def grading_node(state: State) -> dict:
    print("Grading...")
    
    question = state["search_query"]
    context = state["context"]
    is_relevent = check_grading(question, context)

    return {
        "is_relevent": is_relevent
    }

def query_rewrite_node(state: State) -> dict:
    print("Query Rewriting...")

    question = state["question"]
    previous_question = state["search_query"]

    new_query = query_rewritter(question, previous_question)

    print("New Question: ", new_query)

    # Increase retry count
    retry_count = state["retry_count"] + 1

    print(f"Attempt Retry: {retry_count}/{MAX_RETRY_LIMIT}")

    return {
       "search_query": new_query,
       "retry_count": retry_count
    }


def fallback_node(state: State) -> dict:
    print("Fallback...")

    return {
        "answer": "I couldn't find this information in the knowledge base."
    }

# Conditional Node
def route_after_grading(state: State) -> Literal["generation", "fallback", "query_rewriting"]:
    print("Routing...")

    if state["is_relevent"]:
        return "generation"

    if state["retry_count"] < MAX_RETRY_LIMIT:
        return "query_rewriting"
    
    return "fallback"
    

# Graph Builder
builder = StateGraph(State)

# Register Nodes
builder.add_node("retrieval", retrieval_node)
builder.add_node("generation", generation_node)
builder.add_node("grading", grading_node)
builder.add_node("query_rewriting", query_rewrite_node)
builder.add_node("fallback", fallback_node)

# Connect Edges
builder.add_edge(START, "retrieval")
builder.add_edge("retrieval", "grading")
builder.add_conditional_edges("grading", route_after_grading, {
    "generation": "generation",
    "query_rewriting": "query_rewriting",
    "fallback": "fallback"
})
builder.add_edge("query_rewriting", "retrieval")
builder.add_edge("generation", END)
builder.add_edge("fallback", END)

graph = builder.compile()

def call_rag(question):
    state = {
        "question": question,
        "search_query": question,
        "context": "",
        "answer": "",
        "is_relevent": False,
        "retry_count": 0
    }

    result = graph.invoke(state)

    return result["answer"]
