from collections import OrderedDict
from functools import lru_cache

import jinja2
import markdown
import cherrypy

from . import models as m
from . import utils, security

conf_default = object()


class VoteApplication(object):

    def __init__(self, config):
        self._config = config

        m.database.init(self.conf('database', 'file'))

        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.conf('templating', 'directory')))
        self.template_env.globals.update(
            site_name='Searching For The Perfect System',
            base_url = self.conf('general', 'base_url'))
        self.template_env.filters.update({
            'dewidow': utils.dewidow
            })

    def bind_routes(self, routes):
        for url, component_factory in routes.items():
            component = component_factory(app=self)
            setattr(self, url, component)

    @lru_cache(maxsize=None)
    def conf(self, section, key, default=conf_default):
        if default is not conf_default:
            if not (section in self._config and key in self._config[section]):
                return default

        return eval(self._config[section][key])

    def drop_tables(self):
        m.database.drop_tables(m.tables, safe=True)

    def create_tables(self):
        m.database.create_tables(m.tables, safe=True)

    def insert_data(self, data):

        systems = data['systems']
        for sys in systems.values():

            bite = "".join("<li>" + utils.dewidow(i) + "</li>" for i in sys['information'])
            bite = "<ul>" + bite + "</ul>"

            text = utils.double_paragraphs(sys['description'])
            text = markdown.markdown(text)

            db_system = m.System.create(name=sys['name'], bite=bite, data=text)
            for link in sys.get('links', []):
                m.Link.create(system=db_system, name=link['name'],
                                    link=link['site'])

            sys['loaded'] = db_system

        questions = data['questions']
        for question in questions.values():
            db_question = m.Question.create(text=question['text'],
                                            description=question['explanation'])

            for answer in question['answers'].values():
                ans = m.Answer.create(question=db_question, text=answer['text'])
                for system in answer['systems']:
                    ans.systems.add(systems[system]['loaded'])
                ans.save()
