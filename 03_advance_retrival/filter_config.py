from qdrant_client.models import Filter, FieldCondition, MatchValue

def create_metadata_config(topic=None, file_type=None):
    conditions = []

    if topic:
        conditions.append(
            FieldCondition(
                key="metadata.topic",
                match=MatchValue(
                    value=topic
                )
            )
        )

    if file_type:
        conditions.append(
            FieldCondition(
                key="metadata.file_type",
                match=MatchValue(
                    value=file_type
                )
            )
        )

    if not conditions:
        return None

    filter_metadata = Filter(
        must=conditions
    )

    return filter_metadata