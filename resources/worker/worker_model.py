from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, ListField, ReferenceField, BooleanField, FloatField, \
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


class WorkerHandles(EmbeddedDocument):
    telegram            = StringField()
    slack               = StringField()
    discord             = StringField()
    facebook            = StringField()
    allo                = StringField()
    hangouts            = StringField()


class Worker(Document):
    username            = EmbeddedDocumentField(WorkerHandles)
    reputation          = FloatField(default=1)
    email               = EmailField()
    credits             = FloatField(default=0)
    properties          = EmbeddedDocumentField(WorkerProperties)
