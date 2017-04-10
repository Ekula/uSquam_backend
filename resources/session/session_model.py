from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentListField,\
    BooleanField, IntField, DateTimeField, ObjectIdField
import datetime
from bson.objectid import ObjectId


SESSION_STATUS = [
    'ACTIVE',
    'ON_HOLD',
    'STOPPED',
    'DONE'
]

class Answer(EmbeddedDocument):
    _id                 = ObjectIdField(required=True, default=lambda: ObjectId() )
    message             = StringField(required=True)
    timestamp           = DateTimeField(default=datetime.datetime.now())
    validated           = BooleanField(default=False)
    #question           = ObjectIdField(required=True)


class Session(Document):
    task_id             = ObjectIdField(required=True)
    # 'review' indicates if the session is for a regular task (false) or review task (true)
    review              = BooleanField(default=False)
    task_data_id        = ObjectIdField(required=True)
    worker_id           = ObjectIdField(required=True)
    state               = IntField(default=0)
    answers             = EmbeddedDocumentListField(Answer)
    # 'validated' indicates if the session has been reviewed
    validated           = BooleanField(default=False)
    status              = StringField(default='ACTIVE', choices=SESSION_STATUS)
