from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

"""
query = "How many people live in Berlin?"

relevent_chunks = [
    "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
    "Berlin has a yearly total of about 135 million day visitors, making it one of the most-visited cities in the European Union.",
    "In 2013 around 600,000 Berliners were registered in one of the more than 2,300 sport and fitness clubs.",
]

# Pair
pairs = [
    (query, document) for document in relevent_chunks
]

# Score
scores = reranker.predict(pairs)

reranked_list = list(
    zip(relevent_chunks, scores)
)

# Sort based on score
reranked_list.sort(
    key=lambda item:item[1],
    reverse=True
)

for document, score in reranked_list:
    print("="*80)
    print("Score", score)
    print("Document \n", document)
"""

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