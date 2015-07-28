import peewee
from playhouse.fields import ManyToManyField


# Database definitions ###################################################################

database = peewee.SqliteDatabase(None)


# Model definitions ######################################################################

class BaseModel(peewee.Model):
    class Meta:
        database = database


class System(BaseModel):
    name = peewee.CharField()
    bite = peewee.TextField()
    bite_md = peewee.TextField()
    data = peewee.TextField()
    data_md = peewee.TextField()

    def __hash__(self):
        return hash(self.id)


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
    arbitrary = peewee.BooleanField(default=True)
    answers = ManyToManyField(Answer, related_name='responses')

ResponseAnswer = Response.answers.get_through_model()

tables = [System, Link, Question, Answer, AnswerSystem, Response, ResponseAnswer]


# Utility Functions ######################################################################

def connection():
    return database.execution_context()


def create_tables(tables=tables, safe=True):
    database.create_tables(tables, safe=safe)


def drop_tables(tables=tables, safe=True):
    database.drop_tables(tables, safe=safe)


def dump_models():
    systems = []
    for system in System.select():
        systems.append({
            'id': system.id,
            'name': system.name,
            'bite': system.bite_md,
            'data': system.data_md
        })

    questions = []
    for question in Question.select():
        answers = []

        for answer in question.answers.select():
            answers.append({
                'id': answer.id,
                'text': answer.text,
                'systems': [sys.id for sys in answer.systems.select()]
            })

        questions.append({
            'id': question.id,
            'text': question.text,
            'desc': question.description,
            'answers': answers
        })

    return (systems, questions)


def load_models(systems, questions, markdown):
    with connection():
        for sys_data in systems:
            try:
                system = System.get(id=sys_data['id'])
            except System.DoesNotExist:
                system = System.create(id=sys_data['id'], name=sys_data['name'],
                                       bite_md=sys_data['bite'], bite=markdown(sys_data['bite']),
                                       data_md=sys_data['data'], data=markdown(sys_data['data']))
            else:
                system.name = sys_data['name']
                system.bite_md = sys_data['bite']
                system.bite = markdown(system.bite_md)
                system.data_md = sys_data['data']
                system.data = markdown(system.data_md)
                system.save()

        for qu_data in questions:
            try:
                question = Question.get(id=qu_data['id'])
            except Question.DoesNotExist:
                question = Question.create(id=qu_data['id'],
                                           text=qu_data['text'],
                                           description=qu_data['desc'])
            else:
                question.text = qu_data['text']
                question.description = qu_data['desc']
                question.save()

            for answer_data in qu_data['answers']:
                try:
                    answer = Answer.get(id=answer_data['id'])
                except Answer.DoesNotExist:
                    answer = Answer.create(id=answer_data['id'],
                                           text=answer_data['text'],
                                           question=question)
                else:
                    answer.text = answer_data['text']
                    answer.question = question
                    answer.save()

                answer.systems.clear()
                for system_id in answer_data['systems']:
                    system = System.get(id=system_id)
                    answer.systems.add(system)
                answer.save()
