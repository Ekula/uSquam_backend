from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentListField,\
    BooleanField, IntField, DateTimeField, ObjectIdField, DictField
import datetime
from bson.objectid import ObjectId


SESSION_STATUS = [
    'ACTIVE',
    'ON_HOLD',
    'STOPPED',
    'DONE'
]

SESSION_TYPES = [
    'TASK',
    'IDLE',
    'REVIEW'
]

class Answer(EmbeddedDocument):
    _id                 = ObjectIdField(required=True, default=lambda: ObjectId() )
    message             = StringField(required=True)
    timestamp           = DateTimeField(default=datetime.datetime.now())
    validated_answer    = StringField()
    #question           = ObjectIdField(required=True)


class Session(Document):
    task_id             = ObjectIdField(required=True)
    task_data_id        = ObjectIdField()
    worker_id           = ObjectIdField(required=True)
    type                = StringField(default='TASK', choices=SESSION_TYPES)
    state               = IntField(default=0)
    answers             = EmbeddedDocumentListField(Answer)
    validated           = BooleanField(default=False)
    status              = StringField(default='ACTIVE', choices=SESSION_STATUS)
    cache               = DictField()
