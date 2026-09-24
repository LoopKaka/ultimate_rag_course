from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

def rerank_document(question, relevent_chunks, top_k=5):
    documents = [
        document for document, score in relevent_chunks
    ]

    # Pair
    pairs = [
       (question, document.page_content) for document in documents
    ]

    # Score
    scores = reranker.predict(pairs)

    # attcah with document
    ranked_list = list(
        zip(documents, scores)
    )

    # Sort based on score
    ranked_list.sort(
        key=lambda item:item[1],
        reverse=True
    )

    return ranked_list[:top_k]