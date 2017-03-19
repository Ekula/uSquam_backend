from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField, IntField, DateTimeField


class Data(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ReferenceField('resources.requester.requester_model.Requester', required=True)
    entries             = ListField(StringField)
