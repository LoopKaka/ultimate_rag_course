from pathlib import Path
import json
from statistics import mean
import time
from config import (
    JUDGE_RAG_MODEL, EVALUATE_RAG_COLLECTION, INPUT_COST_GPT_4_1_MINI,
    OUTPUT_COST_GPT_4_1_MINI
)
from rag import generate_llm_answer
from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.metrics import Faithfulness, ContextRecall, FactualCorrectness
from ragas.llms import llm_factory
from openai import AsyncOpenAI
import pandas as pd

DATASET_DIR = "05_rag_evaluation_optimization/dataset_evaluation.json"
REPORT_OUTPUT_DIR = "05_rag_evaluation_optimization/"

def calculate_llm_cost(input_tokens, output_tokens):
    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_GPT_4_1_MINI

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_GPT_4_1_MINI

    return input_cost + output_cost

with Path(DATASET_DIR).open("r", encoding="UTF-8") as file:
    dataset_list = json.load(file)


def evaluate_rag(item, top_k):
    question_id = item['id']
    question = item['question']
    relevent_chunk_ids = set(item['relevent_chunk_ids'])
    ground_truth = item['ground_truth']

    # Calculate latency
    start_time = time.perf_counter()
    # Generate Answer
    response = generate_llm_answer(question, top_k)
    end_time = time.perf_counter()

    latency = end_time - start_time

    retrieved_chunk_ids = response['retrieved_chunk_ids']
    generated_answer = response['answer']
    retrieved_context = response['context']

    #Calculate Cost
    input_tokens = response["input_tokens"]
    output_tokens = response["output_tokens"]
    cost = calculate_llm_cost(input_tokens, output_tokens)

    return {
        "id": question_id,
        "question": question,
        "relevent_chunk_ids": relevent_chunk_ids,
        "ground_truth": ground_truth,
        "generated_answer": generated_answer,
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "retrieved_context": retrieved_context,
        "latency": round(latency, 2),
        "cost": round(cost, 4)
    }

def evaluate_rag_top_k(top_k):
    ragas_rows = []
    results = []
    for item in dataset_list:
        result = evaluate_rag(item, top_k)

        row = SingleTurnSample(
            user_input=result["question"],
            reference=result["ground_truth"],
            response=result["generated_answer"],
            retrieved_contexts=[result["retrieved_context"]]
        )

        ragas_rows.append(row)
        results.append(result)

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

    scores_df['cost'] = [result['cost'] for result in results]
    scores_df['latency'] = [result['latency'] for result in results]

    avg_faithfulness = (scores_df['faithfulness']).mean()
    avg_context_recall = (scores_df['context_recall']).mean()
    avg_factual_correctness = (scores_df['factual_correctness(mode=f1)']).mean()

    avg_cost = mean(
        result['cost'] for result in results
    )

    avg_latency = mean(
        result['latency'] for result in results
    )

    results = json.loads(
        scores_df.to_json(orient="records", force_ascii=False)
    )

    summery = {
        "collection_name": EVALUATE_RAG_COLLECTION,
        "dataset_name": "dataset_evaluation.json",
        "retrieval_mode": "HYBRID",
        "total_questions": len(dataset_list),
        "top_k": top_k,
        "mean": {
            "faithfulness": avg_faithfulness,
            "context_recall": avg_context_recall,
            "factual_correctness": avg_factual_correctness,
            "cost": avg_cost,
            "latency": avg_latency
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

    with Path(REPORT_OUTPUT_DIR + f"top_k_{top_k}_cost_latency.json").open("w", encoding="UTF-8") as file:
        json.dump(convert_sort(report), file, indent=2, ensure_ascii=False)
        print("Report Generated")

    return summery


summeries = [
    evaluate_rag_top_k(k)
    for k in [3, 5, 8]
]

comparison = []
for result in summeries:
    comparison.append({
        "top_k": result["top_k"],
        **result["mean"]
    })

comparison_df = pd.DataFrame(comparison)
comparison_path = REPORT_OUTPUT_DIR + "final_report_top_k_latency_cost.csv"
comparison_df.to_csv(comparison_path, index=False)
print("Final Report Generated")
