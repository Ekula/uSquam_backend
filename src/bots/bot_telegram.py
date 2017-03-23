from telegram.ext import Updater, CommandHandler, MessageHandler
from utils.secrets import TELEGRAM_KEY
from src.interaction_redirector import InteractionRedirector
from flask import request, jsonify, json
from resources.task.service import TaskService
import random
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    result = InteractionRedirector.onInput(update.message.from_user.id, 'start')
    update.message.reply_text(result)

def task(bot, update, args):
    result = InteractionRedirector.onInput(update.message.from_user.id, 'task')
    update.message.reply_text(result)

def tasks(bot, update):
    all_tasks = TaskService.getAll()
    result = ""
    for t in all_tasks:
        result += '{}, '.format(t.name)
    update.message.reply_text(result)

def message(bot, update):
    result = InteractionRedirector.onInput(update.message.from_user.id, update.message.text)
    update.message.reply_text(result)

def start_telegram_bot():
    print 'Get the updater'
    updater = Updater(TELEGRAM_KEY)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('task', task, pass_args=True,))
    updater.dispatcher.add_handler(CommandHandler('tasks', tasks))
    updater.dispatcher.add_handler(MessageHandler(None, message))

    return updater