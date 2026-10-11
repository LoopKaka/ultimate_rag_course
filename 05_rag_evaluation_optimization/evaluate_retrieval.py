from pathlib import Path
import json
from statistics import mean
from retrieval import retrive_chunks
from config import (EVALUATE_RAG_COLLECTION)

DATASET_DIR = "05_rag_evaluation_optimization/dataset_evaluation.json"
REPORT_OUTPUT_DIR = "05_rag_evaluation_optimization/retieval_evaluation_report.json"
TOP_K = 5

with Path(DATASET_DIR).open("r", encoding="UTF-8") as file:
    dataset_list = json.load(file)

def evaluate(item):
    question_id = item['id']
    question = item['question']
    relevent_chunk_ids = set(item['relevent_chunk_ids'])

    # Retrive Chunks
    documents = retrive_chunks(question, TOP_K)

    retrieved_chunk_ids = []
    for document, _ in documents:
        chunk_id = document.metadata["chunk_id"]
        retrieved_chunk_ids.append(chunk_id)

    retrieved_chunk_ids_set = set(retrieved_chunk_ids)

    # Intersection to find out common chunks
    matched_chunk_ids = retrieved_chunk_ids_set.intersection(relevent_chunk_ids)

    # Calculate Hit Rates
    hit_rate = 1.0 if matched_chunk_ids else 0.0

    # Calculate Recall
    recall = len(matched_chunk_ids) / len(relevent_chunk_ids)

    # Calculate Reciprocal Rank
    reciprocal_rank = 0.0
    for rank, chunk_id in enumerate(retrieved_chunk_ids, start=1):
        if chunk_id in relevent_chunk_ids:
            reciprocal_rank = 1.0/rank
            break

    return {
        "question_id": question_id,
        "question": question,
        "relevent_chunk_ids": relevent_chunk_ids,
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "matched_chunk_ids": matched_chunk_ids,
        "hit_rate": hit_rate,
        "recall": recall,
        "reciprocal_rank": reciprocal_rank,
        "documents": [
            {
                "rank": rank,
                "page_content": document.page_content
            }
            for rank, (document, _) in enumerate(documents)
        ]
    }


results = []

for item in dataset_list:
    result = evaluate(item)
    results.append(result)

    print("="*60)
    print("Question Id", result["question_id"])
    print("Question", result["question"])
    print("  -   Hit Rate", result["hit_rate"])
    print("  -   Recall", result["recall"])
    print("  -   Reciprocal Rank", result["reciprocal_rank"])

hit_rate_at_k = mean(
    result["hit_rate"] for result in results
)

recall_at_k = mean(
    result["recall"] for result in results
)

mrr_at_k = mean(
    result["reciprocal_rank"] for result in results
)

summery = {
    "collection_name": EVALUATE_RAG_COLLECTION,
    "dataset_name": "dataset_evaluation.json",
    "retrieval_mode": "HYBRID",
    "total_questions": len(dataset_list),
    "hit_rate_at_k": hit_rate_at_k,
    "recall_at_k": recall_at_k,
    "mrr_at_k": mrr_at_k
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
