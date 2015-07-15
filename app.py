from configparser import ConfigParser
import sqlite3
import cherrypy
from votes import VoteApplication, DatabasePlugin, components, utils

config = ConfigParser()
config.read('votes.conf')
config.read('votes-private.conf')

application = VoteApplication(data=utils.ordered_load('data.yml'), config=config,
    routes={
        'index': components.Static.factory(page='index.html'),
        'about': components.Static.factory(page='about.html'),
        'quiz': components.Quiz.factory(),
        'results': components.Results.factory(),
        'systems': components.Systems.factory(),
        'static': components.Assets.factory()
    }
)

DatabasePlugin(cherrypy.engine, application).subscribe()
cherrypy.quickstart(application, '/', 'votes.conf')
