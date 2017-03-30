from flask import Flask
import utils.database 
from resources.register import api_bp
from src.bots.bot_telegram import start_telegram_bot
from multiprocessing import Process, Manager
from utils.mongoengine_jsonencoder import MongoEngineJSONEncoder
from time import sleep
from flask_bcrypt import Bcrypt
import argparse
from flask import jsonify
import os

app = Flask(__name__)
app.json_encoder = MongoEngineJSONEncoder
app.register_blueprint(api_bp)
app.bcrypt = Bcrypt(app)

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
parser.add_argument('--deploy', action='store_true')

@app.route('/')
def index():
    return jsonify({'status': 200, 'success':True})

if __name__ == "__main__":
    # Detect if app has restarted in debug mode - else the chat bot will try to start multiple times
    if 'WERKZEUG_RUN_MAIN' in os.environ:
        updater = start_telegram_bot()
        updater.start_polling()

    debugMode = parser.parse_args().debug
    deployMode = parser.parse_args().deploy

    if deployMode:
        app.run(host='0.0.0.0', debug=debugMode, use_reloader=debugMode)
    else:
        app.run(debug=debugMode, use_reloader=debugMode)

    if updater is not None:
        updater.stop()