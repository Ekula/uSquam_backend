from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ListField, ReferenceField, \
    BooleanField, FloatField,  DateTimeField, ObjectIdField, CASCADE, IntField, PointField
from resources.session.session_model import Answer 
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
    data_collection_id  = ObjectIdField()
    questions           = EmbeddedDocumentListField(Question)
    time_indication     = FloatField(required=True)
    reward              = FloatField(required=True)
    active              = BooleanField(default=False)
    date_modified       = DateTimeField(default=datetime.datetime.now)
    coordinates         = PointField()
    
class ReviewTask(Document):
    task_id             = ObjectIdField(required=True)
    task_data_id        = ObjectIdField(required=True)
    worker_id           = ObjectIdField(required=True)
    original_session    = ObjectIdField(required=True)
    reward              = FloatField(required=True)
    questions           = EmbeddedDocumentListField(Question)
    answers             = EmbeddedDocumentListField(Answer)

class Action(EmbeddedDocument):
    intent              = StringField()
    action              = StringField()

class State(EmbeddedDocument):
    question            = StringField()
    actions             = EmbeddedDocumentListField(Action)

class IdleTask(Document):
    name               = StringField(required=True, unique=True)
    states             = EmbeddedDocumentListField(State)
