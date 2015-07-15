import peewee
from playhouse.fields import ManyToManyField

database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class System(BaseModel):
    name = peewee.CharField()
    bite = peewee.TextField()
    data = peewee.TextField()


class Link(BaseModel):
    system = peewee.ForeignKeyField(System, related_name='links')
    name = peewee.CharField()
    link = peewee.CharField()


class Question(BaseModel):
    text = peewee.CharField()
    description = peewee.TextField()


class Answer(BaseModel):
    question = peewee.ForeignKeyField(Question, related_name='answers')
    text = peewee.CharField()
    systems = ManyToManyField(System)

AnswerSystem = Answer.systems.get_through_model()


class Response(BaseModel):
    answers = ManyToManyField(Answer)

ResponseAnswer = Response.answers.get_through_model()


tables = [System, Link, Question, Answer, AnswerSystem, Response, ResponseAnswer]
