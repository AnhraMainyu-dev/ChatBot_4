from telegram import KeyboardButton, ReplyKeyboardMarkup, Update


def start_game_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Начать игру!")],
        ],
        resize_keyboard=True,
    )


def play_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Новый вопрос"), KeyboardButton(text="Сдаться")],
            [KeyboardButton(text="Мой счёт")],
        ],
        resize_keyboard=True,
    )
