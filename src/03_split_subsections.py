import json
import re


input_file = "../processed/ElectricMotorController-RAG_sections.json"
output_file = "../processed/ElectricMotorController-RAG_subsections.json"


with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    sections = json.load(f)


subsections = []


def is_heading(line):
    """
    Определяем, является ли строка заголовком
    """

    line = line.strip()

    if not line:
        return False


    # Заголовки вида:
    # 1.1 Общие сведения
    # 2.3 Подключение контроллера

    if re.match(r"^\d+\.\d+", line):
        return True


    # Ручные заголовки

    headings = [
        "Подключение ручек газа/тормоза",
        "PWM сигнал",
        "Подключение переключателя направления движения",
        "Подключения датчиков положения ротора электромотора",
        "Подключение ON/OFF",
        "Подключение Bluetooth модуля или ПК",
        "Установка приложения",
        "Включение контроллера",
        "Соединения с Андроид приложением",
        "Соединения с ПК приложением",
        "Пользовательский интерфейс",
    ]


    if line in headings:
        return True


    return False



for section in sections:

    chapter = section["section"]
    text = section["text"]


    lines = text.split("\n")


    current_title = chapter
    current_text = []


    for line in lines:


        if is_heading(line):


            # сохраняем предыдущий блок

            if current_text:

                subsections.append(
                    {
                        "section": chapter,
                        "topic": current_title,
                        "text": "\n".join(current_text).strip()
                    }
                )


            current_title = line.strip()

            current_text = []


        else:

            current_text.append(line)



    # последний блок

    if current_text:

        subsections.append(
            {
                "section": chapter,
                "topic": current_title,
                "text": "\n".join(current_text).strip()
            }
        )



with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        subsections,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Готово!")
print("Создано подразделов:", len(subsections))