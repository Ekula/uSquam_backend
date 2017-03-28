from mongoengine import Document, EmbeddedDocument, StringField, ObjectIdField, EmbeddedDocumentListField, IntField
from bson.objectid import ObjectId


DATA_TYPE = [
    'TEXT',
    'IMAGE',
    'URL'
]


class DataItem(EmbeddedDocument):
    _id                 = ObjectIdField( required=True, default=lambda: ObjectId())
    content             = StringField(required=True)
    # Todo: List of Dynamic (embedded) document or DictField?
    # So that someone cn define 'imageUrl1 = 'http://www...', imageUrl2
    # Then we need to format their question, e.g. "Which image would you prefer? {imageUrl1} {imageUrl2}
    # But most chat messengers send images as separate messages, so maybe just defining order of data?
    # Let's first just simply implement 1 data entry that is sent when the task is started...

    # Todo: Define data type per item of per DataEntry?


# Todo: Rename to DataCollection
class Data(Document):
    name                = StringField(required=True, max_length=30)
    requester_id        = ObjectIdField(required=True)
    items               = EmbeddedDocumentListField(DataItem)



