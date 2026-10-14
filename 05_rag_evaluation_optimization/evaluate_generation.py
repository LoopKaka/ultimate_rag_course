from pathlib import Path
import json
from statistics import mean
from config import (
    TOP_K, JUDGE_RAG_MODEL, EVALUATE_RAG_COLLECTION
)
from rag import generate_llm_answer
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

DATASET_DIR = "05_rag_evaluation_optimization/dataset_evaluation.json"
REPORT_OUTPUT_DIR = "05_rag_evaluation_optimization/generation_evaluation_report.json"

with Path(DATASET_DIR).open("r", encoding="UTF-8") as file:
    dataset_list = json.load(file)


class GenerationScore(BaseModel):
    correctness: int = Field(
        ge=0, le=5,
        description="How correct the generation answer is compared with the reference answer."
    )

    faithfulness: int = Field(
        ge=0, le=5,
        description="How well the generated answer is supported by the supplied retrieved context."
    )

    answer_relevance: int = Field(
        ge=0, le=5,
        description="How directly and completely the answer addresses the user's question."
    )

    correctness_reason: str = Field(
        description="One concise sentence."
    )

    faithfulness_reason: str = Field(
        description="One concise sentence."
    )

    answer_relevance_reason: str = Field(
        description="One concise sentence."
    )

judge_llm = ChatOpenAI(
    model=JUDGE_RAG_MODEL,
    temperature=0
)

structured_judge_llm = judge_llm.with_structured_output(
    GenerationScore
)

JUDGE_PROMPT = """
You are an objective evaluator for a RAG system.
Evaluate the Generated Answer against the Question, 
Ground Truth (Reference Answer), and Retrieved Context.

**Scoring Rubric (0 to 5):**
- Correctness (0-5): How accurately the Generated Answer aligns with the Ground Truth and Context. Give 0 if it contradicts the Ground Truth or if Ground Truth explicitly marks it incorrect. Give 5 ONLY if fully accurate against Ground Truth and Context.
- Faithfulness (0-5): How strictly the Generated Answer is derived ONLY from the Retrieved Context. Give 0 if facts are completely unmentioned or hallucinated relative to the Context.
- Answer Relevance (0-5): How directly the Generated Answer answers the Question. Give 0 if off-topic or completely unhelpful.

**Strict Guidelines:**
1. Ground Truth is the absolute source of truth for Correctness. Do not ignore or override Ground Truth.
2. If Ground Truth states "Wrong answer", the Correctness score MUST be 0.
3. Be strict: Penalize missing details, inaccuracies, or unsupported facts.
4. Keep all reasoning explanations under 20 words.

Inputs:
Question: {question}
Ground Truth: {ground_truth}
Retrieved Context: {retrieved_context}
Generated Answer: {generated_answer}
"""

def evaluate(item):
    question_id = item['id']
    question = item['question']
    ground_truth = item['ground_truth']

    # Generate Answer From RAG
    response = generate_llm_answer(question, TOP_K)

    generated_answer = response['answer']
    retrieved_context = response['context']

    prompt = JUDGE_PROMPT.format(
        question=question,
        ground_truth=ground_truth,
        retrieved_context=retrieved_context,
        generated_answer=generated_answer
    )

    scores = structured_judge_llm.invoke(prompt)

    return {
        "question_id": question_id,
        "question": question,
        "ground_truth": ground_truth,
        "generated_answer": generated_answer,
        "score": {
            "correctness": scores.correctness,
            "faithfulness": scores.faithfulness,
            "answer_relevance": scores.answer_relevance
        },
        "normalized_score": {
            "correctness": scores.correctness / 5,
            "faithfulness": scores.faithfulness / 5,
            "answer_relevance": scores.answer_relevance / 5
        },
        "reason": {
            "correctness": scores.correctness_reason,
            "faithfulness": scores.faithfulness_reason,
            "answer_relevance": scores.answer_relevance_reason
        }
    }


results = []
for item in dataset_list:
    result = evaluate(item)
    results.append(result)

    print("="*60)
    print("Question Id", result["question_id"])
    print("Question", result["question"])
    print("Score: ")
    print("        - correctness    ", result["score"]["correctness"])
    print("        - faithfulness    ", result["score"]["faithfulness"])
    print("        - answer_relevance    ", result["score"]["answer_relevance"])


avg_correctness = mean(
    result["score"]["correctness"] for result in results
)

avg_faithfulness = mean(
    result["score"]["faithfulness"] for result in results
)

avg_answer_relevance = mean(
    result["score"]["answer_relevance"] for result in results
)

summery = {
    "collection_name": EVALUATE_RAG_COLLECTION,
    "dataset_name": "dataset_evaluation.json",
    "retrieval_mode": "HYBRID",
    "total_questions": len(dataset_list),
    "avg_correctness": avg_correctness,
    "avg_faithfulness": avg_faithfulness,
    "avg_answer_relevance": avg_answer_relevance
}

report = {
    "summery": summery,
    "results": results
}

def convert_sort(value):
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, dict):
        return {key: convert_sort(item) for key, item in value.items()}
    if isinstance(value, list):
        return [convert_sort(item) for item in value]
    return value

with Path(REPORT_OUTPUT_DIR).open("w", encoding="UTF-8") as file:
    json.dump(convert_sort(report), file, indent=2, ensure_ascii=False)
    print("Report Generated")
