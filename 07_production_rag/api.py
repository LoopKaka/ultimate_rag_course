from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langgraph_rag import call_rag

class RagRequest(BaseModel):
    question: str = Field(min_length=1)

class RagResponse(BaseModel):
    question: str
    answer: str

app = FastAPI(
    title="LoopKaka's RAG Course"
)

@app.get("/")
def health():
    return {
        "status": "ok"
    }

@app.post("/ask", response_model=RagResponse)
def ask(request: RagRequest):
    try:
        question = request.question
        answer = call_rag(question)

        return RagResponse(
            question=question,
            answer=answer
        )
    except Exception as err:
        return HTTPException(
            status_code=500,
            detail=f"Request is not processed: {err}"
        )
