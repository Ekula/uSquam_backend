from flask import Flask
import utils.database 
from resources.register import api_bp
from src.bots.bot_telegram import updater
from multiprocessing import Process, Manager
from utils.mongoengine_jsonencoder import MongoEngineJSONEncoder
from time import sleep
import argparse

app = Flask(__name__)
app.json_encoder = MongoEngineJSONEncoder
app.register_blueprint(api_bp)

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')

if __name__ == "__main__":
    updater.start_polling()
    app.run(debug=parser.parse_args().debug)
    updater.stop()