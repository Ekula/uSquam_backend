from telegram.ext import Updater, CommandHandler
from utils.secrets import TELEGRAM_KEY
from resources.task.service import TaskService

def start(bot, update):
    update.message.reply_text('Hello World')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )

updater = Updater(TELEGRAM_KEY)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('task', hello))