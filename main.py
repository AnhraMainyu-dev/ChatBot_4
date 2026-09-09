from telegram.ext import Application, CommandHandler, MessageHandler, filters
from decouple import config
from tg_handlers import start, echo

def main():
    tg_token = config("TG_TOKEN")
    vk_api = config('VK_API')

    app = Application.builder().token(tg_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == '__main__':
    main()
