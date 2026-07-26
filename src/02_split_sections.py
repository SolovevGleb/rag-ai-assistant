import re
from pathlib import Path
import json


input_file = Path("../processed/ElectricMotorController-RAG_text.txt")
output_file = Path("../processed/ElectricMotorController-RAG_sections.json")


# читаем текст
text = input_file.read_text(
    encoding="utf-8"
)


# ищем главы
pattern = r"(Глава\s+\d+.*?)(?=Глава\s+\d+|$)"


sections = re.findall(
    pattern,
    text,
    flags=re.S
)


result = []


for section in sections:

    # название первой строки
    title = section.split("\n")[0]

    result.append(
        {
            "section": title.strip(),
            "text": section.strip()
        }
    )


with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Создано разделов:", len(result))