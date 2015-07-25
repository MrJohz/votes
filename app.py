from configparser import ConfigParser
import sqlite3

import cherrypy

from votes import VoteApplication, components, utils

config = ConfigParser()
config.read('votes.conf')

app = VoteApplication(config=config)

app.bind_routes({
    'index': components.Static.factory(page='site/index.html'),
    'about': components.Static.factory(page='site/about.html'),
    'quiz': components.Quiz.factory(hasher=app.hasher),
    'results': components.Results.factory(hasher=app.hasher),
    'systems': components.Systems.factory(),
    'static': components.Assets.factory(),
    'admin': components.admin.AdminInterface.factory()})

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        cherrypy.quickstart(app, '/', 'votes.conf')
    elif sys.argv[1] == 'setup-database':
        app.drop_tables()
        app.create_tables()
        app.insert_data(utils.ordered_load(app.conf('general', 'data_source_file')))
