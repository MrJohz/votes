from configparser import ConfigParser
import sqlite3
import cherrypy
from votes import VoteApplication, components, utils

config = ConfigParser()
config.read('votes.conf')
config.read('votes-private.conf')

app = VoteApplication(config=config,
    routes={
        'index': components.Static.factory(page='index.html'),
        'about': components.Static.factory(page='about.html'),
        'quiz': components.Quiz.factory(),
        'results': components.Results.factory(),
        'systems': components.Systems.factory(),
        'static': components.Assets.factory()
    }
)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        cherrypy.quickstart(app, '/', 'votes.conf')
    elif sys.argv[1] == 'setup-database':
        app.drop_tables()
        app.create_tables()
        app.insert_data(utils.ordered_load(app.conf('general', 'source_file')))
