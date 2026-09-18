from hy_retrieve_dense import dense_retrive_chunks
from hy_retrieve_sparse import sparse_retrive_chunks

def get_document_id(document):
    metadata = document.metadata or {}
    return (
        metadata.get("_id")
        or metadata.get("document_id")
        or metadata.get("source")
        or document.page_content
    )

def reciprocal_rank_fusion(results_lists, k=60):
    scores = {}
    documents = {}

    for results in results_lists:
        for rank, (document, _retrieval_score) in enumerate(results, start=1):
            document_id = get_document_id(document)
            score = 1/(k+rank)
            documents[document_id] = document
            scores[document_id] = (
                scores.get(document_id, 0) + score
            )

    fused_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [(documents[document_id], score) for document_id, score in fused_scores]

if __name__ == "__main__":
    question = input("You: ")
    dense_results = dense_retrive_chunks(question)
    sparse_results = sparse_retrive_chunks(question)

    results = reciprocal_rank_fusion([dense_results, sparse_results])

    for index, (document, score) in enumerate(results):
        print("="*80)
        print("Chunk No: ", index+1)
        print("-"*80)
        print("Content: ", document.page_content, "\n")
        print("RRF Score: ", score, "\n")
