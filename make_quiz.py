def make_quiz():
    with open(".materials/drakon10.txt", "r", encoding="KOI8-R") as file:
        file_content = file.read()

    quiz = {}
    question = None

    parts = file_content.split("\n\n")
    for part in parts:
        part = part.strip()
        if "\n" not in part:
            continue

        header, text = part.split("\n", 1)
        text = " ".join(text.split())

        if header.startswith("Вопрос"):
            question = text
        elif header.startswith("Ответ"):
            quiz[question] = text

    return quiz
