from mongoengine import Document, EmbeddedDocument, StringField, ObjectIdField, EmbeddedDocumentListField
from bson.objectid import ObjectId


DATA_TYPE = [
    'TEXT',
    'IMAGE',
    'URL'
]

class QuestionData(EmbeddedDocument):
    type                = StringField(choices=DATA_TYPE,required=True)
    content             = StringField(required=True)


class TaskData(EmbeddedDocument):
    _id                 = ObjectIdField( required=True, default=lambda: ObjectId())
    items               = EmbeddedDocumentListField(QuestionData)


class DataCollection(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    items               = EmbeddedDocumentListField(TaskData)



