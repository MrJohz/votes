import contextlib
import cherrypy

from . import models


def parse_params(resource_id, action):
    if resource_id is None:
        resource_id = 'get'
    resource_id, action = (i.lower() for i in (resource_id, action))
    if resource_id in ('get', 'post'):
        return (None, resource_id)

    try:
        resource_id = int(resource_id)
    except ValueError:
        raise cherrypy.NotFound()

    return (resource_id, action)


class DatabaseTool(cherrypy.Tool):

    def __init__(self):
        super().__init__('before_handler', self.load_db)

    def _setup(self):
        super()._setup()
        cherrypy.request.hooks.attach('before_finalize', self.end_db)

    def load_db(self):
        models.database.connect()

    def end_db(self):
        try:
            models.database.close()
        except:
            pass

cherrypy.tools.database_connect = DatabaseTool()


class ComponentFactory(object):

    exposed = False

    def __init__(self, component, *args, **kwargs):
        self._component = component
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args = self._args + args
        kwargs.update(self._kwargs)
        return self._component(*args, **kwargs)


class BaseComponent(object):

    exposed = True

    def __init__(self, app, config=None):
        self.app = app

        if config is not None:
            if hasattr(self, '_cp_config'):
                self._cp_config.update(config)
            else:
                self._cp_config = config

        for key in dir(self):
            component = getattr(self, key)
            if isinstance(component, ComponentFactory):
                setattr(self, key, component(app=app))

    def template(self, template_name, **kwargs):
        return self.app.template_env.get_template(template_name).render(**kwargs)

    @property
    @contextlib.contextmanager
    def db(self):
        with models.database.execution_context() as ctx:
            yield

    @classmethod
    def factory(cls, **kwargs):
        return ComponentFactory(cls, **kwargs)


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


class RestfulComponent(BaseComponent):

    def GET(self, resource_id=None, action='get'):
        resource_id, action = parse_params(resource_id, action)

        if (resource_id, action) == (None, 'get'):
            return self.get()
        elif (resource_id, action) == (None, 'post'):
            return self.post()
        elif resource_id is not None and action == 'put':
            return self.put(resource_id)
        elif resource_id is not None and action == 'delete':
            return self.delete(resource_id)
        else:
            raise cherrypy.NotFound()

    def POST(self, resource_id=None, action='get', **form):
        resource_id, action = parse_params(resource_id, action)

        if (resource_id, action) == (None, 'get'):
            raise cherrypy.HTTPError(405, 'Method not implemented')
        elif (resource_id, action) == (None, 'post'):
            return self.do_post(form)
        elif resource_id is not None and action == 'put':
            return self.do_put(resource_id, form)
        elif resource_id is not None and action == 'delete':
            return self.do_delete(resource_id, form)
        else:
            raise cherrypy.NotFound()


class Static(BaseComponent):

    def __init__(self, page, args=None, *pargs, **kwargs):
        super(Static, self).__init__(*pargs, **kwargs)
        self.page = page
        self.args = args
        if self.args is None:
            self.args = {}

    def GET(self):
        return self.template(self.page, **self.args)
