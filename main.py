import datetime
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

TOKEN: Final = '6422765606:AAGBvW2RUfgb2yM0JIf_nTjiPs8m0_f6vgU'
BOT_USERNAME: Final = '@paradeStateSurvey_bot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is the Parade State Bot')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Parade State Bot and will account for the parade state everyday to serve my country! Use /parade to test the full polling of the bot.')


async def scheduled_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    """ Running on Sun, Mon, Tue, Wed, Thu = tuple(range(5)) at 10:00 UTC time (8 pm SGT) """
    t = datetime.time(hour=12, minute=00, second=00)
    # t = datetime.time(hour=6, minute=20, second=00)
    
    # *** A Warning will be sent to the console log but it will still work; IGNORE IT ***
    context.job_queue.run_daily(paradeState_call, t, days=(
        0, 1, 2, 3, 4), data=None, name=None, chat_id=chat_id)

    print('Starting Scheduled Parade State')
    await update.message.reply_text('Starting Scheduled Parade State')


async def paradeState_call(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job

    today = date.today()

    tommorrow = today + datetime.timedelta(days=1)

    # array of options for parade state poll
    reports = ["PRESENT", "RSO/MC", "RSI",
               "LEAVE (AM/PM)", "OFF (AM/PM)", "DUTY", "MA (AM)", "MA (PM)", "COURSE", "OTHERS"]

    # array of branches in Base HQ
    branches = ['S1 🫂', 'S3 🔫', 'S4 💸']

    message = await context.bot.send_poll(
        job.chat_id,
        "📋 Parade State for " + branches[2] + ' ' + str(tommorrow),
        reports,
        is_anonymous=False,
        allows_multiple_answers=False,
    )

    """Sends polls for all branches in SBC"""
    # for branch in branches:
    #     message = await context.bot.send_poll(
    #     job.chat_id,
    #     "📋 Parade State for " + branch + ' ' + today,
    #     reports,
    #     is_anonymous=False,
    #     allows_multiple_answers=False,
    # )


async def paradeState_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: deploy to website server and create command to print the status of the parade state
    today = date.today()

    tommorrow = today + datetime.timedelta(days=1)

    # array of options for parade state poll
    reports = ["PRESENT", "RSO/MC", "RSI", "LEAVE (AM/PM)",
               "OFF (AM/PM)", "DUTY", "MA (AM)", "MA (PM)", "COURSE",  "OTHERS"]

    # array of branches in Base HQ
    branches = ['S1 🫂', 'S3 🔫', 'S4 💸']

    message = await context.bot.send_poll(
        update.effective_chat.id,
        "📋 Parade State for " + branches[2] + ' ' + str(tommorrow),
        reports,
        is_anonymous=False,
        allows_multiple_answers=False,
    )

    """Sends polls for all branches in SBC"""
    # for branch in branches:
    #     message = await context.bot.send_poll(
    #     update.effective_chat.id,
    #     "📋 Parade State for " + branch + ' ' + str(tommorrow),
    #     reports,
    #     is_anonymous=False,
    #     allows_multiple_answers=False,
    # )

# Handling all other messages


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    job = context.job

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
    await context.bot.send_message(job.chat_id, text=response)
    # await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')

if __name__ == '__main__':
    print('Starting Parade State Bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('parade', paradeState_command))
    app.add_handler(CommandHandler('scheduled', scheduled_command))

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error handling
    app.add_error_handler(error)

    # checking updates in chat
    print('Polling...')
    app.run_polling(poll_interval=3)
