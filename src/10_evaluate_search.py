import json

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer



# модель embedding

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)



# Qdrant

client = QdrantClient(
    path="../data/qdrant"
)


collection_name = "mv85500"



# вопросы

with open(
    "../tests/questions.json",
    "r",
    encoding="utf-8"
) as f:
    questions = json.load(f)



top1 = 0
top3 = 0



for item in questions:

    question = item["question"]
    expected = item["expected_topic"]


    # embedding вопроса

    vector = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()



    # поиск

    results = client.query_points(
        collection_name=collection_name,
        query=vector,
        limit=3
    ).points



    found_topics = []


    for r in results:

        found_topics.append(
            r.payload["metadata"]["topic"]
        )


    print("\n====================")
    print("Вопрос:")
    print(question)

    print("\nОжидалось:")
    print(expected)


    print("\nНашли:")

    for i, topic in enumerate(found_topics):

        print(
            i+1,
            topic,
            "score:",
            round(results[i].score,3)
        )



    # проверка

    if expected == found_topics[0]:
        top1 += 1


    if expected in found_topics:
        top3 += 1



print("\n\n========== ИТОГО ==========")

print(
    "Top-1:",
    top1,
    "/",
    len(questions)
)

print(
    "Top-3:",
    top3,
    "/",
    len(questions)
)



client.close()