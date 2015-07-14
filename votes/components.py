from urllib.parse import urlencode
from functools import partial
from collections import Counter

from cherrypy import HTTPRedirect

from . import utils

__all__ = ['BaseComponent', 'Quiz', 'Results', 'Systems', 'static_page', 'Static']


class BaseComponent(object):

    def __init__(self, data):
        self.data = data

    def template(self, template_name, *args, **kwargs):
        raise NotImplemented()

    @classmethod
    def builder(cls, **kwargs):
        return partial(cls, **kwargs)


class Quiz(BaseComponent):

    winner_kind = utils.QuickEnum(perfect='perfect', best='best')

    def determine(self, results):
        system_votes = Counter()
        system_opportunities = Counter()
        for question_id, answer_id in results.items():
            if question_id not in self.data['questions']:
                continue
            elif answer_id == 'ignore':
                continue

            answers = data['questions'][question_id]['answers']
            if answer_id not in answers:
                continue

            for sys in answers[answer_id]['systems']:
                system_votes[sys] += 1

            for answer in answers.values():
                for sys in answer['systems']:
                    system_opportunities[sys] += 1

        vote_percentage = [()]
        return self.winner_kind.perfect, ['fptp']

    def GET(self):
        return self.template('questions.html')

    def POST(self, **kwargs):
        winner_kind, systems = self.determine(kwargs)
        querystr = urlencode({'winner': winner_kind, 'systems': ','.join(systems)})
        url = '/results?' + querystr
        raise HTTPRedirect(url)


class Results(object):

    def GET(self, arg):
        return self.template('results.html')
