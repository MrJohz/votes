import peewee
from playhouse.fields import ManyToManyField
import datetime

database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class System(BaseModel):
    name = peewee.CharField()
    bite = peewee.TextField()
    bite_md = peewee.TextField()
    data = peewee.TextField()
    data_md = peewee.TextField()


class Link(BaseModel):
    system = peewee.ForeignKeyField(System, related_name='links')
    name = peewee.CharField()
    link = peewee.CharField(unique=True)


class Question(BaseModel):
    text = peewee.CharField()
    description = peewee.TextField()


class Answer(BaseModel):
    question = peewee.ForeignKeyField(Question, related_name='answers')
    text = peewee.CharField()
    systems = ManyToManyField(System, related_name='answers')

AnswerSystem = Answer.systems.get_through_model()


class Response(BaseModel):
    arbitrary = peewee.BooleanField()
    answers = ManyToManyField(Answer, related_name='responses')

ResponseAnswer = Response.answers.get_through_model()


tables = [System, Link, Question, Answer, AnswerSystem, Response, ResponseAnswer]
