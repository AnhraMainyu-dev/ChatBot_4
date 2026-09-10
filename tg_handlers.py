import random

from telegram import Update
from telegram.ext import CallbackContext

from constants import IF_CORRECT, IF_MISTAKEN
from tg_keyboards import play_keyboard, start_game_keyboard

WAIT_QUESTION, WAIT_ANSWER = (1, 2)


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Игра началась",
        reply_markup=start_game_keyboard(),
    )

    return WAIT_QUESTION


async def handle_new_question_request(update: Update, context: CallbackContext):
    quiz = context.bot_data["quiz"]
    question = random.choice(list(quiz))
    db = context.bot_data["db"]
    db.set(update.effective_chat.id, question)
    context.bot_data["current_question"] = question

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=question,
        reply_markup=play_keyboard(),
    )

    return WAIT_ANSWER


async def handle_solution_attempt(update: Update, context: CallbackContext):
    answer = update.message.text
    db = context.bot_data["db"]
    quiz = context.bot_data["quiz"]
    current_question = db.get(update.effective_chat.id)
    correct_answer = quiz[current_question].split(".")[0]

    if answer.lower() == correct_answer.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=IF_CORRECT,
            reply_markup=play_keyboard(),
        )
        return WAIT_QUESTION
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=IF_MISTAKEN,
        )
        return WAIT_ANSWER


async def handle_give_up(update: Update, context: CallbackContext):
    question = context.bot_data["current_question"]
    quiz = context.bot_data["quiz"]
    correct_answer = quiz[question]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Правильный ответ: {correct_answer}\nПопробуй следующий вопрос!",
        reply_markup=play_keyboard(),
    )

    return WAIT_QUESTION
