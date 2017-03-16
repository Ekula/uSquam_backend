from flask import Flask
import utils.database 
from resources.register import api_bp
from src.bots.bot_telegram import updater
from multiprocessing import Process, Manager
from utils.mongoengine_jsonencoder import MongoEngineJSONEncoder
from time import sleep

app = Flask(__name__)
app.json_encoder = MongoEngineJSONEncoder
app.register_blueprint(api_bp)

if __name__=="__main__":
    updater.start_polling()
    app.run()
    updater.stop()