class VoteApplication(object):

    def __init__(self, **kwargs):
        for url, component_factory in kwargs.items():
            url = '/' + url
            component = component_factory(parent=self)
            component.exposed = True
            component.url = url
            setattr(self, component)
