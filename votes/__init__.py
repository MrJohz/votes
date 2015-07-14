from collections import OrderedDict
from functools import lru_cache

import jinja2

class VoteApplication(object):

    def __init__(self, data, config, routes):
        self._config = config
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.conf('templating', 'directory')))
        self.template_env.globals.update(
            site_name='Searching For The Perfect System',
            questions=data['questions'],
            systems=OrderedDict(sorted(data['systems'].items())))
        self.template_env.filters.update({
            'dewidow': (lambda x: '&nbsp;'.join(x.rsplit(' ', 1))
                if len(x.split(' ')) > 3 else x)
            })

        for url, component_factory in routes.items():
            component = component_factory(app=self, data=data)
            component.exposed = True
            component.url = url
            setattr(self, url, component)

    @lru_cache(maxsize=None)
    def conf(self, section, key):
        return eval(self._config[section][key])
