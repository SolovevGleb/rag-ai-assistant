import json


input_file = "../processed/ElectricMotorController-RAG_subsections.json"
output_file = "../processed/ElectricMotorController-RAG_subsections_clean.json"


with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)


clean = []


for item in data:

    text = item["text"].strip()
    topic = item["topic"].strip()


    # удаляем пустые блоки
    if len(text) < 50:
        continue


    # удаляем заголовки глав
    if topic.startswith("Глава"):
        continue


    clean.append(item)



with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        clean,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Было:", len(data))
print("Стало:", len(clean))