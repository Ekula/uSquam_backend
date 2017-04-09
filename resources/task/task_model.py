from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ListField, ReferenceField, \
    BooleanField, FloatField,  DateTimeField, ObjectIdField, CASCADE, IntField
import datetime

ANSWER_TYPE = [
    'TEXT',
    'NUMBER',
    'DATE',
    'TIME',
    'DATETIME',
    'IMAGE',
    'LOCATION',
    'SOUND'
    # Money, specific set of choices, etc.
    # Minimum number of chararacters?
]

class Question(EmbeddedDocument):
    message             = StringField(required=True)
    expected_type       = StringField(choices=ANSWER_TYPE)
    suggestions         = ListField(StringField())
    question_data_idx   = IntField()

class Task(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    data_collection_id  = ObjectIdField(required=True)
    questions           = EmbeddedDocumentListField(Question)
    time_indication     = FloatField(required=True)
    gps_based           = BooleanField(default=False)
    reward              = FloatField(required=True)
    active              = BooleanField(default=False)
    date_modified       = DateTimeField(default=datetime.datetime.now)
    
class ReviewTask(session, task):
    task_id                = session['task_id']
    task_data_id           = session['task_data_id']
    worker_id              = session['worker_id']
    questions              = task.questions
    answers                = session.answers
