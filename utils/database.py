from mongoengine import connect

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

connect('usquam', host=MONGODB_HOST, port=MONGODB_PORT)