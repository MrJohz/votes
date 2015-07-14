import cherrypy
from votes import VoteApplication, components, utils

application = VoteApplication(data=utils.ordered_load('data.yml'),
    routes={
        '/quiz': components.Quiz.builder,
        '/results': components.Results.builder,
        '/systems': components.Systems.builder,
        '/index': components.Static.builder(page='index.html'),
        '/about': components.Static.builder(page='about.html')
    }
)

cherrypy.quickstart(application, '/')
