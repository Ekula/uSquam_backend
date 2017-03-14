from telegram.ext import Updater, CommandHandler, MessageHandler
from utils.secrets import TELEGRAM_KEY
from resources.task.service import TaskService
from lib.interaction_manager import InteractionManager

telegramIM = InteractionManager()

def start(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, 'start')
    print result
    update.message.reply_text(result)

def task(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, 'task')
    print result
    update.message.reply_text(result)

def message(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, update.message.text)
    print result
    update.message.reply_text(result)

updater = Updater(TELEGRAM_KEY)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('task', task))
updater.dispatcher.add_handler(MessageHandler(None, message))