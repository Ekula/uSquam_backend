from telegram.ext import Updater, CommandHandler, MessageHandler
from utils.secrets import TELEGRAM_KEY
from src.interaction_redirector import InteractionRedirector
from flask import request, jsonify, json
from resources.task.service import TaskService
import random
import os
import time
import sys
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
    
def sendImage(bot, update):
    bot.sendPhoto(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png');
    
def fetchContent(bot, update):
    updates = bot.getUpdates()
    
def downloadFile(bot):
    file_id = update.message.photo[-1]
    newFile = bot.getFile(file_id)
    newFile.download('image.jpg')
    
def message(bot, update):
    result = InteractionRedirector.onInput(update.message.from_user.id, update.message.text)
    update.message.reply_text(result)

# buttons: List, n_cols: int, header_buttons: List = none, footer_buttons: List = none
def build_menu(buttons, n_cols = 0, header_buttons = None, footer_buttons = None):                 
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def get_data_buttons(bot):
    button_list = [
    InlineKeyboardButton("col 1", arg1),
    InlineKeyboardButton("col 2", arg2),
    InlineKeyboardButton("row 2", arg3)
    ]
    reply_markup = ReplyKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    message(bot, "A two column menu", reply_markup)
    
def restart(bot, update):
    bot.sendMessage(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

def start_telegram_bot():
    print 'Get the updater'
    updater = Updater(TELEGRAM_KEY)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('task', task, pass_args=True,))
    updater.dispatcher.add_handler(CommandHandler('tasks', tasks))
    updater.dispatcher.add_handler(MessageHandler(None, message))

    return updater