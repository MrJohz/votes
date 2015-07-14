import os

from urllib.parse import urlencode
from functools import partial
from collections import Counter

import cherrypy

from . import utils, quiz

__all__ = ['BaseComponent', 'Quiz', 'Results', 'Systems', 'static_page', 'Static']

_BC_SENTINEL = object()

class BaseComponent(object):

    def __init__(self, app, data):
        self.app = app
        self.data = data

    def template(self, template_name, **kwargs):
        kwargs.update(questions=self.data['questions'])
        return self.app.template_env.get_template(template_name).render(**kwargs)

    @classmethod
    def factory(cls, **kwargs):
        return partial(cls, **kwargs)


class Quiz(BaseComponent):

    def GET(self):
        return self.template('questions.html')

    def POST(self, **kwargs):
        winner_kind, systems, votes = quiz.determine(self.data, kwargs)
        querystr = urlencode({'winner': winner_kind, 'systems': ','.join(systems)})
        url = '/results?' + querystr
        raise cherrypy.HTTPRedirect(url)


class Results(BaseComponent):

    def GET(self, winner, systems):
        return self.template('results.html', winner=winner, systems=systems)


class Systems(BaseComponent):

    def GET(self, system=None):
        if system is None:
            return self.template('systems.html')
        else:
            if system in self.data['systems']:
                sys = self.data['systems'][system]
                return self.template('system.html', system=sys)
            else:
                raise cherrypy.NotFound()


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
        if self.app.conf('static', 'on_the_fly_compile'):
            scss_dir = self.app.conf('static', 'css_source_dir')
        directory = self.app.conf('static', 'css_dir')
        return cherrypy.lib.static.serve_file(os.path.join(directory, asset))
