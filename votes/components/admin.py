import contextlib
import cherrypy

from .base import BaseComponent, Static
from .. import models

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
    return [s for s in strist if s.strip()]


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
            return self.template('admin/modify_system.html')
        elif system_id is not None and action == 'put':
            return self.template('admin/modify_system.html',
                                 system=get_model_instance(system_id, models.System))
        elif system_id is not None and action == 'delete':
            return self.template('admin/delete_system.html',
                                 system=get_model_instance(system_id, models.System))
        else:
            raise cherrypy.NotFound()

    def POST(self, system_id=None, action='get', **form):
        system_id, action = parse_params(system_id, action, ('post', 'get'))

        if (system_id, action) == (None, 'post'):
            form['links'] = zip(destr(form.get('l-name')), destr(form.get('l-url')))
            system = models.System.create(
                name=form.get('name'),
                bite_md=form.get('bite'),
                bite=self.app.markdown(form.get('bite', '')),
                data_md=form.get('desc'),
                data=self.app.markdown(form.get('desc', '')))

            for name, link in form['links']:
                models.Link.insert(system=system, name=name, link=link).execute()
            raise cherrypy.HTTPRedirect("/systems/" + str(system.id))
        elif system_id is not None and action == 'put':
            form['links'] = zip(destr(form.get('l-name')), destr(form.get('l-url')))
            system = get_model_instance(system_id, models.System)
            if form.get('name') and form['name'].strip():
                system.name = form['name']
            if form.get('bite') and form['bite'].strip():
                system.bite_md = form['bite']
                system.bite = self.app.markdown(form['bite'])
            if form.get('desc') and form['desc'].strip():
                system.data_md = form['desc']
                system.data = self.app.markdown(form['desc'])

            system.save()

            models.Link.delete().where(models.Link.system == system).execute()
            for name, link in form['links']:
                models.Link.insert(system=system, name=name, link=link).execute()

            raise cherrypy.HTTPRedirect('/admin/systems/' + str(system_id) + '/put')
        elif system_id is not None and action == 'delete':
            if form.get('delete', '').lower() == 'yes':
                pass

        else:
            raise cherrypy.NotFound()


class AdminInterface(AuthenticatedComponent):
    index = Static.factory(page='admin/index.html')
    systems = SystemInterface.factory()
