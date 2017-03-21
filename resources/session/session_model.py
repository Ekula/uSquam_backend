from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentListField,\
    BooleanField, IntField, DateTimeField
import datetime


SESSION_STATUS = [
    'ACTIVE',
    'ON_HOLD',
    'STOPPED',
    'DONE'
]


class Answer(EmbeddedDocument):
    message             = StringField(required=True)
    timestamp           = DateTimeField(default=datetime.datetime.now())
    question            = ReferenceField('resources.task.task_model.Question')


class Session(Document):
    task_id             = ReferenceField('resources.task.task_model.Task', required=True)
    worker_id           = ReferenceField('resources.worker.worker_model.Worker', required=True)
    state               = IntField(default=0)
    answers             = EmbeddedDocumentListField(Answer)
    status              = StringField(required=True, choices=SESSION_STATUS)



