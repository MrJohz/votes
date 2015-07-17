import contextlib

from . import models


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

    def __init__(self, app):
        self.app = app

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

    def __init__(self, page, *args, **kwargs):
        super(Static, self).__init__(*args, **kwargs)
        self.page = page

    def GET(self):
        return self.template(self.page)
