import json
from sentence_transformers import SentenceTransformer


input_file = "../processed/ElectricMotorController-RAG_chunks_context.json"
output_file = "../processed/ElectricMotorController-RAG_embeddings.json"


# Загружаем embedding модель
model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)


# Загружаем чанки
with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)


print("Чанков загружено:", len(chunks))


# Создаем вектора
for i, chunk in enumerate(chunks):

    text = chunk["text"]


    embedding = model.encode(
        text,
        normalize_embeddings=True
    )


    # numpy -> list
    chunk["embedding"] = embedding.tolist()


    print(
        f"{i+1}/{len(chunks)} готов"
    )


# сохраняем

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Готово!")
print(
    "Создан файл:",
    output_file
)