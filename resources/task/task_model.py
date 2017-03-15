from mongoengine import Document, StringField

class Task(Document):
    name = StringField(required=True, max_length=30)
