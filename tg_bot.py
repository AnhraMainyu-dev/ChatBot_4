import redis
from decouple import config
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from make_quiz import make_quiz
from tg_handlers import (WAIT_ANSWER, WAIT_QUESTION, handle_give_up,
                         handle_new_question_request, handle_solution_attempt,
                         start)


def main():
    tg_token = config("TG_TOKEN")
    vk_api = config("VK_API")

    quiz = make_quiz()
    db = redis.Redis(host="localhost", port=6379, decode_responses=True)

    app = Application.builder().token(tg_token).build()
    app.bot_data["quiz"] = quiz
    app.bot_data["db"] = db

    order_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAIT_QUESTION: [
                MessageHandler(
                    filters.Regex("Начать игру!"), handle_new_question_request
                ),
                MessageHandler(
                    filters.Regex("Новый вопрос"), handle_new_question_request
                ),
            ],
            WAIT_ANSWER: [
                MessageHandler(filters.Regex("Сдаться"), handle_give_up),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, handle_solution_attempt
                ),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(order_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
