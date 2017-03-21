from mongoengine import Document, EmbeddedDocument, StringField, ObjectIdField, EmbeddedDocumentListField
from bson.objectid import ObjectId


class DataEntry(EmbeddedDocument):
    _id                 = ObjectIdField( required=True, default=lambda: ObjectId())
    content             = StringField(required=True)


class Data(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    items               = EmbeddedDocumentListField(DataEntry)



