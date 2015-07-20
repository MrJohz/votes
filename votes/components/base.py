import contextlib

from . import models


class DatabaseTool(cherrypy.Tool):

    def __init__(self):
        super().__init__(self, 'before_handler', self.load_db)

    def _setup(self):
        super()._setup()
        cherrypy.request.hooks.attach('before_finalize', self.end_db)

    def load_db(self):
        models.database.connect()

    def end_db(self):
        models.database.close()

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


class Static(BaseComponent):

    def __init__(self, page, args=None, *pargs, **kwargs):
        super(Static, self).__init__(*pargs, **kwargs)
        self.page = page
        self.args = args
        if self.args is None:
            self.args = {}

    def GET(self):
        return self.template(self.page, **self.args)
