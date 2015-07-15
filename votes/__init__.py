from collections import OrderedDict
from functools import lru_cache

import jinja2

from . import models as m

conf_default = object()


class VoteApplication(object):

    def __init__(self, config, routes):
        self._config = config

        m.database.init(self.conf('database', 'file'))

        #self.template_env = jinja2.Environment(
        #    loader=jinja2.FileSystemLoader(self.conf('templating', 'directory')))
        #self.template_env.globals.update(
        #    site_name='Searching For The Perfect System',
        #    questions=data['questions'],
        #    systems=OrderedDict(sorted(data['systems'].items())))
        #self.template_env.filters.update({
        #    'dewidow': (lambda x: '&nbsp;'.join(x.rsplit(' ', 1))
        #        if len(x.split(' ')) > 3 else x)
        #    })

        for url, component_factory in routes.items():
            component = component_factory(app=self)
            component.exposed = True
            component.url = url
            setattr(self, url, component)

    @lru_cache(maxsize=None)
    def conf(self, section, key, default=conf_default):
        value = self._config[section].get(key)
        if value is None and default is not conf_default:
            return default
        else:
            return eval(self._config[section][key])

    def drop_tables(self):
        m.database.drop_tables(m.tables, safe=True)

    def create_tables(self):
        m.database.create_tables(m.tables, safe=True)

    def insert_data(self, data):
        to_markdown = lambda x: x.replace('\n', '\n\n').strip()

        systems = data['systems']
        for sys in systems.values():
            db_system = m.System.create(name=sys['name'], bite=sys['information'],
                                        data=to_markdown(sys['description']))
            for link in sys.get('links', []):
                m.Link.create(system=db_system, name=link['name'],
                                    link=link['site'])

            sys['loaded'] = db_system
            db_system.save()

        questions = data['questions']
        for question in questions.values():
            db_question = m.Question.create(text=question['text'],
                                            description=question['explanation'])

            for answer in question['answers'].values():
                ans = m.Answer.create(question=db_question, text=answer['text'])
                for system in answer['systems']:
                    ans.systems.add(systems[system]['loaded'])
                ans.save()
            db_question.save()
