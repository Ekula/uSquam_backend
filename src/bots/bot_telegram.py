from telegram.ext import Updater, CommandHandler, MessageHandler
from utils.secrets import TELEGRAM_KEY
from resources.task.service import TaskService
from src.interaction_redirector import InteractionRedirector

telegramIM = InteractionRedirector()

def start(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, 'start')
    update.message.reply_text(result)

def task(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, 'task')
    update.message.reply_text(result)

def message(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, update.message.text)
    update.message.reply_text(result)

updater = Updater(TELEGRAM_KEY)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('task', task))
updater.dispatcher.add_handler(MessageHandler(None, message))