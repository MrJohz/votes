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
        if not results:
            raise ValueError("Need at least one result to use")

        system_votes = Counter()
        system_opportunities = Counter()
        for question_id, answer_id in results.items():
            if question_id not in self.data['questions']:
                continue
            elif answer_id == 'ignore':
                continue

            answers = self.data['questions'][question_id]['answers']
            if answer_id not in answers:
                continue

            for sys in answers[answer_id]['systems']:
                system_votes[sys] += 1

            for answer in answers.values():
                for sys in answer['systems']:
                    system_opportunities[sys] += 1

        votes = []
        for sys in self.data['systems']:
            if system_opportunities[sys] > 0:
                votes.append((system_votes[sys] / system_opportunities[sys], sys))
        votes.sort()

        if not votes:  # impossible?
            raise ValueError("No votes counted")

        perfect = []
        best = []
        for vote in votes:
            if vote[0] == 1:
                perfect.append(vote)
            elif perfect:
                break
            elif not best or vote[0] >= best[0][0]:
                best.append(vote)
            else:
                break

        if perfect:
            return self.winner_kind.perfect, [i[1] for i in perfect], votes
        else:
            return self.winner_kind.best, [i[1] for i in best], votes

    def GET(self):
        return self.template('questions.html')

    def POST(self, **kwargs):
        winner_kind, systems, votes = self.determine(kwargs)
        querystr = urlencode({'winner': winner_kind, 'systems': ','.join(systems)})
        url = '/results?' + querystr
        raise HTTPRedirect(url)


class Results(object):

    def GET(self, arg):
        return self.template('results.html')
