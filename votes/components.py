from urllib.parse import urlencode
from functools import partial

from cherrypy import HTTPRedirect

from . import utils

__all__ = ['BaseComponent', 'Quiz', 'Results', 'Systems', 'static_page', 'Static']


class BaseComponent(object):

    def __init__(self, parent):
        self.parent = parent

    def template(self, template_name, *args, **kwargs):
        raise NotImplemented()

    @classmethod
    def builder(cls, **kwargs):
        return partial(cls, **kwargs)


class Quiz(object):

    winner_kind = utils.QuickEnum(perfect='perfect', best='best')

    def determine(self, results):
        return self.winner_kind.perfect, ['fptp']

    def GET(self):
        return self.template('questions.html')

    def POST(self, **kwargs):
        winner_kind, systems = self.determine(kwargs)
        querystr = urlencode('winner': winner_kind, 'systems': ','.join(systems))
        url = ''.join((self.parent.results.url, '?', querystr))
        raise HTTPRedirect(url)


class Results(object):

    def GET(self, arg):
        return self.template('results.html')
