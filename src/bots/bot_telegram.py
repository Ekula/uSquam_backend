from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, Location
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
logger = logging.getLogger(__name__)

def start(bot, update):
    result = InteractionRedirector.onInput(update.message.from_user.id, 'hi')
    update.message.reply_text(result['answer'])

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

    # Check answer type
    if update.message.text is not '':
        result = InteractionRedirector.onInput(update.message.from_user.id, update.message.text)
    elif update.message.location is not None:
        geo_loc = {'latitude': update.message.location.latitude, 'longitude': update.message.location.longitude}
        result = InteractionRedirector.onInput(update.message.from_user.id, geo_loc)
    elif update.message.photo is not None and len(update.message.photo) > 0:
        last_photo = update.message.photo[-1]
        result = InteractionRedirector.onInput(update.message.from_user.id, last_photo.file_id)
    else:
        # Error: Input type is not recognized, send an empty string
        result = InteractionRedirector.onInput(update.message.from_user.id, ' ')

    reply_markup = None

    # Custom options for worker input (buttons, location, photo)
    if 'suggestions' in result:
        buttons = []
        for suggestion in result['suggestions']:
            buttons.append(KeyboardButton(suggestion))
        reply_markup = ReplyKeyboardMarkup([buttons], one_time_keyboard=True)
    if 'location' in result and result['location'] is True:
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Send location", request_location=True),
                                           KeyboardButton("Cancel")]], one_time_keyboard=True)
    if 'send_location' in result:
        # loc = Location(result['send_location']['latitude'], result['send_location']['longitude'])
        update.message.reply_location(latitude=result['send_location']['latitude'],
                                      longitude=result['send_location']['longitude'])

    # Normal text
    update.message.reply_text(
        text=result['answer'],
        reply_markup=reply_markup
    )

def parseLocation(bot, update):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

# buttons: List, n_cols: int, header_buttons: List = none, footer_buttons: List = none
def build_menu(buttons, n_cols = 0, header_buttons = None, footer_buttons = None):                 
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def askGPSlocation(bot):
    message(bot, "For the following task I need to know your location. Could you send me your location?")
    location(bot, update)
    
def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location

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

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start_telegram_bot():
    print 'Get the updater'
    updater = Updater(TELEGRAM_KEY)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(CommandHandler('task', task, pass_args=True,))
    # updater.dispatcher.add_handler(CommandHandler('tasks', tasks))
    updater.dispatcher.add_handler(MessageHandler(None, message))
    updater.dispatcher.add_error_handler(error)
    return updater
