from mongoengine import Document, StringField, FloatField, EmailField

class Requester(Document):
    name            = StringField(required=True, max_length=30)
    password        = StringField(required=True)
    email           = EmailField(required=True, unique=True)
    credits         = FloatField(default=0) # Todo: Not modifiable by owner

