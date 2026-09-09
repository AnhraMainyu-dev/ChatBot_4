from telegram import Update
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Оу май!')

async def echo(update: Update, context: CallbackContext):
    message = update.message.text
    await update.message.reply_text(message)