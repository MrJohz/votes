import os
import contextlib

from urllib.parse import urlencode
from functools import partial
from collections import Counter

import cherrypy
import sass
import peewee

from . import utils, quiz, models

__all__ = ['BaseComponent', 'Quiz', 'Results', 'Systems', 'static_page', 'Static']

_BC_SENTINEL = object()

class BaseComponent(object):

    def __init__(self, app):
        self.app = app

    def template(self, template_name, **kwargs):
        return self.app.template_env.get_template(template_name).render(**kwargs)

    @property
    @contextlib.contextmanager
    def db(self):
        with models.database.execution_context() as ctx:
            yield

    @classmethod
    def factory(cls, **kwargs):
        return partial(cls, **kwargs)


class Quiz(BaseComponent):

    def __init__(self, hasher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasher = hasher

    def GET(self):
        with self.db:
            questions = peewee.prefetch(models.Question.select(), models.Answer.select())
            return self.template('questions.html', questions=questions)

    def POST(self, **kwargs):
        with self.db:
            response = models.Response.create(arbitrary=False)
            for question_id, answer_id in kwargs.items():
                try:
                    question_id = int(question_id)
                    answer_id = int(question_id)
                except ValueError:
                    continue

                try:
                    answer = models.Answer.get(id=answer_id)
                except models.Answer.DoesNotExist:
                    continue

                if answer.question.id != question_id:
                    continue

                response.answers.add(answer)
            response.save()

        url = '/results/' + self.hasher.encode(response.id)
        raise cherrypy.HTTPRedirect(url)


class Results(BaseComponent):

    def __init__(self, hasher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasher = hasher

    def GET(self, hash_id):
        try:
            (response_id,) = self.hasher.decode(hash_id)
        except ValueError:
            raise cherrypy.NotFound()

        response = models.Response.get(id=response_id)
        return self.template('results.html', response=response)


class Systems(BaseComponent):

    def GET(self, sys_id=None):
        if sys_id is None:
            return self.template('systems.html', systems=models.System.select())
        else:
            try:
                system = models.System.get(id=sys_id)
            except models.System.DoesNotExist:
                raise cherrypy.NotFound()

            return self.template('system.html', system=system)


class Static(BaseComponent):

    def __init__(self, page, *args, **kwargs):
        super(Static, self).__init__(*args, **kwargs)
        self.page = page

    def GET(self):
        return self.template(self.page)


class Assets(BaseComponent):

    def GET(self, kind, asset):
        asset = os.path.basename(asset)

        if kind == 'js' and os.path.splitext(asset)[1] == '.js':
            return self.get_javascript(asset)
        elif kind == 'css' and os.path.splitext(asset)[1] == '.css':
            return self.get_css(asset)
        else:
            raise cherrypy.NotFound()

    def get_javascript(self, asset):
        directory = self.app.conf('static', 'javascript_dir')
        return cherrypy.lib.static.serve_file(os.path.join(directory, asset))

    def get_css(self, asset):
        directory = self.app.conf('static', 'css_dir')
        css_path = os.path.join(directory, asset)

        if self.app.conf('static', 'on_the_fly_compile', True):
            scss_dir = self.app.conf('static', 'css_source_dir')
            scss_asset = os.path.splitext(asset)[0] + '.scss'
            scss_path = os.path.join(scss_dir, scss_asset)
            try:
                if os.stat(scss_path).st_mtime > os.stat(css_path).st_mtime:
                    css_source = sass.compile(filename=scss_path)
                    with open(css_path, mode='w') as f:
                        f.write(css_source)
            except:
                msg = 'Failed attempt to compile {src} to {dest}'
                cherrypy.log(msg.format(src=scss_path, dest=css_path), traceback=True)

        return cherrypy.lib.static.serve_file(css_path)
