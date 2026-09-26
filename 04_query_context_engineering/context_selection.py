def select_context(
        reranked_chunks=None,
        top_k=5,
        score_threshold=None
):
    if not reranked_chunks:
        return []

    selected_chunks = []

    for document, score in reranked_chunks:
        if score_threshold is not None and score_threshold > score:
            continue

        selected_chunks.append((document, score))

        if len(selected_chunks) == top_k:
            break

    return selected_chunks

