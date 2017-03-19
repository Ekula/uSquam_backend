from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocumentListField, BooleanField, FloatField, IntField, CASCADE

class Requester(Document):


    name            = StringField(required=True, max_length=30)
    password        = StringField(required=True, min_length=6, max_length=30) # Todo: hashing (flask.ext.Bcrypt)
    email           = StringField(required=True, max_length=30)
    credits         = FloatField(default=0) # Todo: Not modifiable by owner
    tasks           = ListField(ReferenceField('resources.task.task_model.Task', reverse_delete_rule=CASCADE))
