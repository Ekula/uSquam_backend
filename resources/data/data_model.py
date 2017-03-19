from mongoengine import Document, StringField, ListField, ObjectIdField, BooleanField, IntField, DateTimeField


class Data(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    entries             = ListField(StringField())
