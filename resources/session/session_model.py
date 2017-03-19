from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentListField,\
    BooleanField, IntField, DateTimeField
from resources.task.task_model import *
from resources.worker.worker_model import *
import datetime


SESSION_STATUS = [
    'ACTIVE'
    'ON_HOLD'
    'STOPPED'
    'DONE'
]


class Answer(EmbeddedDocument):
    message             = StringField(required=True)
    timestamp           = DateTimeField(default=datetime.datetime.now())
    question            = ReferenceField(Question)


class Session(Document):
    task_id             = ReferenceField(Task, required=True)
    worker_id           = ReferenceField(Worker, required=True)
    state               = IntField(default=0)
    answers             = EmbeddedDocumentListField(Answer)
    status              = StringField(required=True, choices=SESSION_STATUS)



