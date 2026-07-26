import json

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)


input_file = "../processed/ElectricMotorController-RAG_embeddings.json"


# локальная база Qdrant
client = QdrantClient(
    path="../qdrant"
)


collection_name = "mv85500"



# создаём коллекцию

client.create_collection(
    collection_name=collection_name,

    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    )
)



# читаем embeddings

with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)



points = []


for idx, item in enumerate(data):

    points.append(
        PointStruct(
            id=idx,

            vector=item["embedding"],

            payload={
                "text": item["text"],
                "metadata": item["metadata"]
            }
        )
    )



# загружаем

client.upsert(
    collection_name=collection_name,
    points=points
)


print("Загружено чанков:", len(points))