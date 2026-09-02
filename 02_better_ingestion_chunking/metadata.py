from pathlib import Path
import uuid
from collections import defaultdict

def enrich_document_metadata(document):
    source = document.metadata.get("source", "")

    path = Path(source)

    document.metadata["file_name"] = (path.name)
    document.metadata["file_type"] = (path.suffix.lower().replace(".", ""))
    document.metadata["document_id"] = uuid.uuid4()
    document.metadata["technology"] = (path.name)

    return document

def enrich_chunk_metadata(chunks):
    counter = defaultdict(int)

    for chunk in chunks:
        source = chunk.metadata.get("source", "")

        chunk.metadata["chunk_index"] = (counter[source])
        counter[source] += 1
    return chunks


