import contextlib
import cherrypy

from .base import BaseComponent, Static
from .. import models, security

def parse_params(system_id, action, out_of_order_params=('post', 'get')):
    if system_id is None:
        system_id = 'get'
    system_id, action = (i.lower() for i in (system_id, action))
    if system_id in out_of_order_params:
        return (None, system_id)

    try:
        system_id = int(system_id)
    except ValueError:
        raise cherrypy.NotFound()

    return (system_id, action)


def get_model_instance(model_id, model):
    try:
        return model.get(id=model_id)
    except model.DoesNotExist:
        raise cherrypy.NotFound()


def destr(strist):
    """Convert a thing that may be a string or a list into a list of strings"""
    if strist is None:
        return []
    elif isinstance(strist, str):
        return [strist]
    return strist


class AuthenticatedComponent(BaseComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cp_config = {
            'tools.auth_digest.on': True,
            'tools.auth_digest.realm': 'admin',
            'tools.auth_digest.get_ha1': self._get_ha1(),
            'tools.auth_digest.key': self.app.conf('admin', 'auth_key')
        }

    def _get_ha1(self):
        username = self.app.conf('admin', 'username')
        password = self.app.conf('admin', 'password')
        return cherrypy.lib.auth_digest.get_ha1_dict_plain({username: password})

class SystemInterface(BaseComponent):

    def GET(self, system_id=None, action='get'):
        system_id, action = parse_params(system_id, action, ('post', 'get'))

        if (system_id, action) == (None, 'get'):
            return self.template('admin/systems.html', systems=models.System.select())
        elif (system_id, action) == (None, 'post'):
            return self.template('admin/new_system.html')
        elif action == 'put':
            return self.template('admin/modify_system.html',
                                 system=get_model_instance(system_id, models.System))
        elif action == 'delete':
            return self.template('admin/delete.html')
        else:
            raise cherrypy.NotFound()

    def POST(self, system_id=None, action='get', **form):
        system_id, action = parse_params(system_id, action, ('post', 'get'))

        if (system_id, action) == (None, 'post'):
            form['links'] = zip(destr(form.get('l-name')), destr(form.get('l-url')))
            system = models.System.create(
                name=form.get('name'),
                bite=form.get('bite'),
                data=form.get('desc'))

            for name, link in form['links']:
                models.Link.insert(system=system, name=name, link=link).execute()
            raise cherrypy.HTTPRedirect("/systems/" + str(system.id))
        else:
            raise cherrypy.NotFound()


class AdminInterface(AuthenticatedComponent):
    index = Static.factory(page='admin/index.html')
    systems = SystemInterface.factory()
