import json


input_file = "../processed/ElectricMotorController-RAG_chunks.json"
output_file = "../processed/ElectricMotorController-RAG_chunks_context.json"



with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)



new_chunks = []



for chunk in chunks:

    text = chunk["text"]

    metadata = chunk["metadata"]


    section = metadata["section"]
    topic = metadata["topic"]
    device = metadata["device"]


    # добавляем контекст перед текстом

    enriched_text = f"""
Документ: {device}

Раздел: {section}

Тема: {topic}

Текст:
{text}
""".strip()



    new_chunks.append(
        {
            "text": enriched_text,

            "metadata": metadata
        }
    )



with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        new_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )



print("Готово!")
print("Создано чанков:", len(new_chunks))