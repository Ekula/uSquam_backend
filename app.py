from flask import Flask
import utils.database 
from resources.register import api_bp
from src.bots.bot_telegram import updater
from multiprocessing import Process, Manager
from utils.mongoengine_jsonencoder import MongoEngineJSONEncoder
from time import sleep
from flask_bcrypt import Bcrypt
import argparse
from flask import jsonify

app = Flask(__name__)
app.json_encoder = MongoEngineJSONEncoder
app.register_blueprint(api_bp)
app.bcrypt = Bcrypt(app)

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')

@app.route('/')
def index():
    return jsonify({'status': 200, 'success':True})

if __name__ == "__main__":
    updater.start_polling()
    app.run(debug=parser.parse_args().debug,use_reloader=parser.parse_args().debug)
    updater.stop()