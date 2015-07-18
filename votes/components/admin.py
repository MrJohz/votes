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
        return "authenticated!"


class AdminInterface(AuthenticatedComponent):
    index = Static.factory(page='admin/index.html')
    systems = SystemInterface.factory()
