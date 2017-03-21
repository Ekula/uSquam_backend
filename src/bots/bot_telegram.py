from telegram.ext import Updater, CommandHandler, MessageHandler
from utils.secrets import TELEGRAM_KEY
from resources.task.service import TaskService
from resources.data.service import DataService
from src.interaction_redirector import InteractionRedirector
from flask import request, jsonify, json
import random

telegramIM = InteractionRedirector()

def start(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, 'start')
    update.message.reply_text(result)

def task(bot, update, args):
    # result = telegramIM.onInput(update.message.from_user.id, 'task')
    print 'triggered'
    task_id = int(args[0])
    all_tasks = TaskService.getAll()
    this_task = all_tasks[task_id]
    print this_task.questions[0].data_id
    data = DataService.get(this_task.questions[0].data_id)
    print data

    result = '{} \n {}'.format(this_task.questions[0].message, random.choice(data.items).content)

    update.message.reply_text(result)

def tasks(bot, update):
    all_tasks = TaskService.getAll()
    result = ""
    for t in all_tasks:
        result += '{}, '.format(t.name)
    update.message.reply_text(result)

def message(bot, update):
    result = telegramIM.onInput(update.message.from_user.id, update.message.text)
    update.message.reply_text(result)

updater = Updater(TELEGRAM_KEY)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('task', task, pass_args=True,))
updater.dispatcher.add_handler(CommandHandler('tasks', tasks))
updater.dispatcher.add_handler(MessageHandler(None, message))