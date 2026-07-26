import json

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer



# модель для вопросов

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)



# подключаем Qdrant

client = QdrantClient(
    path="../data/qdrant"
)


collection_name = "mv85500"



# вопрос пользователя

question = "Почему контроллер не включается?"



# создаём embedding вопроса

query_vector = model.encode(
    question,
    normalize_embeddings=True
).tolist()



# поиск

results = client.query_points(
    collection_name=collection_name,

    query=query_vector,

    limit=5
)



print("\nВОПРОС:")
print(question)


print("\nТОП РЕЗУЛЬТАТЫ:\n")



for result in results.points:

    print("===================")

    print(
        "Score:",
        round(result.score, 3)
    )


    print(
        "Тема:",
        result.payload["metadata"]["topic"]
    )


    print(
        result.payload["text"][:300]
    )



client.close()