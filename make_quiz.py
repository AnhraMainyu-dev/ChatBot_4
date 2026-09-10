import os

def make_quiz(directory):
    quiz = {}
    question = None

    for quiz_file in os.listdir(directory):
        quiz_path = os.path.join(directory, quiz_file)
        with open(quiz_path, "r", encoding="KOI8-R") as file:
            file_content = file.read()

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
