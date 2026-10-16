from pathlib import Path
import json
from config import (
    TOP_K, JUDGE_RAG_MODEL, EVALUATE_RAG_COLLECTION
)
from rag import generate_llm_answer
from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.metrics import Faithfulness, ContextRecall, FactualCorrectness
from ragas.llms import llm_factory
from openai import AsyncOpenAI

DATASET_DIR = "05_rag_evaluation_optimization/dataset_evaluation.json"
REPORT_OUTPUT_DIR = "05_rag_evaluation_optimization/ragas_report.json"

with Path(DATASET_DIR).open("r", encoding="UTF-8") as file:
    dataset_list = json.load(file)


def evaluate_rag(item):
    question_id = item['id']
    question = item['question']
    relevent_chunk_ids = set(item['relevent_chunk_ids'])
    ground_truth = item['ground_truth']

    # Generate Answer
    response = generate_llm_answer(question, TOP_K)

    retrieved_chunk_ids = response['retrieved_chunk_ids']
    generated_answer = response['answer']
    retrieved_context = response['context']

    return {
        "id": question_id,
        "question": question,
        "relevent_chunk_ids": relevent_chunk_ids,
        "ground_truth": ground_truth,
        "generated_answer": generated_answer,
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "retrieved_context": retrieved_context
    }

ragas_rows = []
for item in dataset_list:
    result = evaluate_rag(item)

    row = SingleTurnSample(
        user_input=result["question"],
        reference=result["ground_truth"],
        response=result["generated_answer"],
        retrieved_contexts=[result["retrieved_context"]]
    )

    ragas_rows.append(row)

# RAGAS Dataset
dataset = EvaluationDataset(ragas_rows)

client = AsyncOpenAI()
judge_llm = llm_factory(JUDGE_RAG_MODEL, client=client)

# Ragas matrics
metrics = [
    Faithfulness(llm=judge_llm), 
    ContextRecall(llm=judge_llm),
    FactualCorrectness(llm=judge_llm)
]

# Evaluate
scores = evaluate(
    dataset=dataset,
    metrics=metrics
)

scores_df = scores.to_pandas()

avg_faithfulness = (scores_df['faithfulness']).mean()
avg_context_recall = (scores_df['context_recall']).mean()
avg_factual_correctness = (scores_df['factual_correctness(mode=f1)']).mean()

results = json.loads(
    scores_df.to_json(orient="records", force_ascii=False)
)

summery = {
    "collection_name": EVALUATE_RAG_COLLECTION,
    "dataset_name": "dataset_evaluation.json",
    "retrieval_mode": "HYBRID",
    "total_questions": len(dataset_list),
    "mean": {
        "faithfulness": avg_faithfulness,
        "context_recall": avg_context_recall,
        "factual_correctness": avg_factual_correctness
    }
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



