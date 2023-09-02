from typing import Final
from telegram import Update
from datetime import date
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    PollAnswerHandler,
    PollHandler)
import random

TOKEN: Final = '6422765606:AAGBvW2RUfgb2yM0JIf_nTjiPs8m0_f6vgU'
BOT_USERNAME: Final = '@paradeStateSurvey_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is the Parade State Bot')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Parade State Bot and will account for the parade state everyday to serve my country!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is the Parade State Bot')

async def paradeState_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: make pool repeat 3 times for all branches, allow undoing selection, add automatic scheduling to run poll everyday, deploy to website server
    today = str(date.today())

    reports = ["Present", "RSO", "AM Leave", "PM Leave", "MC", "Others"]
    message = await context.bot.send_poll(
        update.effective_chat.id,
        "Parade State for " + today,
        reports,
        is_anonymous=False,
        allows_multiple_answers=False,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_message(new_text)
        else:
            return
    else:
        response: str = handle_message(text)


    print('Bot: ', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')

if __name__ == '__main__':
    print('Starting Parade State Bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('parade', paradeState_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error handling
    app.add_error_handler(error)

    # checking updates in chat
    print('Polling...')
    app.run_polling(poll_interval=3)