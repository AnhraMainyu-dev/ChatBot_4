import random

import redis
import vk_api as vk
from decouple import config
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from constants import IF_CORRECT, IF_MISTAKEN
from make_quiz import make_quiz


def add_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Новый вопрос", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Сдаться", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Мой счёт", color=VkKeyboardColor.PRIMARY)

    return keyboard


def send_message(vk_api, event, message, keyboard):
    vk_api.messages.send(
        peer_id=event.peer_id,
        message=message,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def main():
    vk_token = config("VK_API")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    keyboard = add_keyboard()
    quiz = make_quiz()
    db = redis.Redis(host="localhost", port=6379, decode_responses=True)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
            continue
        if event.text == "Новый вопрос":
            question = random.choice(list(quiz))
            db.set(event.peer_id, question)
            send_message(vk_api, event, question, keyboard)
        elif event.text == "Сдаться":
            current_question = db.get(event.peer_id)
            correct_answer = quiz[current_question]
            text = f"Правильный ответ: {correct_answer}\nПопробуй следующий вопрос!"
            send_message(vk_api, event, text, keyboard)
        elif db.get(event.peer_id) is not None:
            answer = event.text
            current_question = db.get(event.peer_id)
            correct_answer = quiz[current_question].split(".")[0]

            if answer.lower() == correct_answer.lower():
                send_message(vk_api, event, IF_CORRECT, keyboard)
            else:
                send_message(vk_api, event, IF_MISTAKEN, keyboard)
        else:
            text = "Нажмите на кнопку 'Новый вопрос' чтобы начать викторину!"
            send_message(vk_api, event, text, keyboard)


if __name__ == "__main__":
    main()
