import json


input_file = "../processed/ElectricMotorController-RAG_subsections_clean.json"
output_file = "../processed/ElectricMotorController-RAG_chunks.json"


# Максимальный размер чанка
CHUNK_SIZE = 2000


with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    sections = json.load(f)


chunks = []


def split_long_text(text, size):
    """
    Разрезает слишком большой текст
    """
    result = []

    start = 0

    while start < len(text):
        end = start + size
        result.append(text[start:end])
        start = end

    return result



for item in sections:

    section = item["section"]
    topic = item["topic"]
    text = item["text"]


    # разбиваем на абзацы
    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]


    current_chunk = ""


    for paragraph in paragraphs:


        # если абзац сам большой
        if len(paragraph) > CHUNK_SIZE:

            # сначала сохраняем накопленное
            if current_chunk:

                chunks.append(
                    {
                        "text": current_chunk,
                        "metadata": {
                            "source": "MV85500.docx",
                            "device": "MV85500",
                            "section": section,
                            "topic": topic
                        }
                    }
                )

                current_chunk = ""


            # режем большой абзац
            parts = split_long_text(
                paragraph,
                CHUNK_SIZE
            )


            for part in parts:

                chunks.append(
                    {
                        "text": part,
                        "metadata": {
                            "source": "MV85500.docx",
                            "device": "MV85500",
                            "section": section,
                            "topic": topic
                        }
                    }
                )


        else:

            # пробуем добавить абзац
            if len(current_chunk) + len(paragraph) < CHUNK_SIZE:

                current_chunk += (
                    paragraph + "\n"
                )

            else:

                # сохраняем текущий чанк

                chunks.append(
                    {
                        "text": current_chunk.strip(),

                        "metadata": {
                            "source": "MV85500.docx",
                            "device": "MV85500",
                            "section": section,
                            "topic": topic
                        }
                    }
                )

                current_chunk = paragraph + "\n"



    # сохраняем остаток

    if current_chunk:

        chunks.append(
            {
                "text": current_chunk.strip(),

                "metadata": {
                    "source": "MV85500.docx",
                    "device": "MV85500",
                    "section": section,
                    "topic": topic
                }
            }
        )



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
print("Создано чанков:", len(chunks))