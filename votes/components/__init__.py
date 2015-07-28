import os

from urllib.parse import urlencode
from collections import Counter

import cherrypy
import sass
import peewee
import jinja2

from .. import utils, models, quiz
from .base import BaseComponent, Static

from . import admin


class Quiz(BaseComponent):

    def __init__(self, hasher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasher = hasher

    @cherrypy.tools.database_connect()
    def GET(self):
        questions = peewee.prefetch(models.Question.select(), models.Answer.select())
        return self.template('site/questions.html', questions=questions)

    @cherrypy.tools.database_connect()
    def POST(self, **kwargs):
        response = models.Response.create()
        added = []
        for question_id, answer_id in kwargs.items():
            try:
                question_id = int(question_id)
                answer_id = int(answer_id)
            except ValueError:
                continue

            try:
                answer = models.Answer.get(id=answer_id)
            except models.Answer.DoesNotExist:
                continue

            if answer.question.id != question_id:
                continue

            added.append(answer)

        if len(added) == 0:
            raise cherrypy.HTTPRedirect('/systems')
        response.answers.add(added)
        response.save()

        url = '/results/' + self.hasher.encode(response.id)
        raise cherrypy.HTTPRedirect(url)


class Results(BaseComponent):

    def __init__(self, hasher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasher = hasher

    @cherrypy.tools.database_connect()
    def GET(self, hash_id):
        try:
            (response_id,) = self.hasher.decode(hash_id)
            response = models.Response.get(id=response_id)
        except (ValueError, models.Response.DoesNotExist):
            raise cherrypy.NotFound()

        results = quiz.Quiz(response).calculate()
        return self.template('site/results.html', results=results)


class Systems(BaseComponent):

    @cherrypy.tools.database_connect()
    def GET(self, sys_id=None):
        if sys_id is None:
            systems = models.System.select().order_by(peewee.fn.Random())
            return self.template('site/systems.html', systems=systems)
        else:
            try:
                system = models.System.get(id=sys_id)
            except (models.System.DoesNotExist, ValueError):
                raise cherrypy.NotFound()

            return self.template('site/system.html', system=system)


class Assets(BaseComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cp_config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': self.app.conf('static', 'base_dir')
        }
