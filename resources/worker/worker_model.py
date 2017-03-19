from mongoengine import Document, EmbeddedDocument, StringField, ListField, ReferenceField, BooleanField, FloatField, \
    IntField, EmailField, CASCADE

class WorkerProperties(EmbeddedDocument):
    age                 = IntField()
    sex                 = StringField()
    address             = StringField() # Country/GPS
    occupation          = StringField()
    has_car             = BooleanField()
    uses_public_transport = BooleanField()
    income              = IntField()
    job_title           = StringField()
    # etc. etc.


class Worker(Document):
    username            = StringField(required=True, max_length=30) # Todo: List of usernames for all services
    reputation          = FloatField(default=1)
    email               = EmailField()
    credits             = FloatField(default=0)
    properties          = EmbeddedDocument(WorkerProperties, reverse_delete_rule=CASCADE)
    # answers = ...
