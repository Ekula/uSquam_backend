from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ListField, ReferenceField, \
    BooleanField, FloatField,  DateTimeField, ObjectIdField, CASCADE
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
    data_id             = ObjectIdField(required=True)
    message             = StringField(required=True) # Todo: Should also be able to include images
    expected_type       = StringField(choices=ANSWER_TYPE)
    suggestions         = ListField(StringField())


class Task(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    questions           = EmbeddedDocumentListField(Question)
    time_indication     = FloatField(required=True)
    reward              = FloatField(required=True)
    active              = BooleanField(default=False)
    date_modified       = DateTimeField(default=datetime.datetime.now)
