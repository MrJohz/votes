from configparser import ConfigParser
import sqlite3
import string

import cherrypy
import hashids

from votes import VoteApplication, components, utils

config = ConfigParser()
config.read('votes.conf')
config.read('votes-private.conf')

app = VoteApplication(config=config)

hasher = hashids.Hashids(
    salt=app.conf('hashids', 'salt', ''),
    alphabet=app.conf('hashids', 'alphabet', string.ascii_lowercase + string.digits),
    min_length=app.conf('hashids', 'length', 5))

app.bind_routes({
    'index': components.Static.factory(page='index.html'),
    'about': components.Static.factory(page='about.html'),
    'quiz': components.Quiz.factory(hasher=hasher),
    'results': components.Results.factory(hasher=hasher),
    'systems': components.Systems.factory(),
    'static': components.Assets.factory()})

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        cherrypy.quickstart(app, '/', 'votes.conf')
    elif sys.argv[1] == 'setup-database':
        app.drop_tables()
        app.create_tables()
        app.insert_data(utils.ordered_load(app.conf('general', 'data_source_file')))
