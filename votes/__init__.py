from collections import OrderedDict
from functools import lru_cache
import sqlite3

import jinja2

from .plugins import database

conf_default = object()


class DatabasePlugin(database.PooledDatabaseConnections):

    def __init__(self, engine, app):
        super().__init__(engine)
        self.app = app

    def connection_factory(self):
        return sqlite3.connect(self.app.conf('database', 'file'))


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
    def conf(self, section, key, default=conf_default):
        value = self._config[section].get(key)
        if value is None and default is not conf_default:
            return default
        else:
            return eval(self._config[section][key])
