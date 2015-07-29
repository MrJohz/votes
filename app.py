from configparser import ConfigParser
import json
import cherrypy
from votes import create_app, components

config = ConfigParser()
config.read('votes.conf')

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        cherrypy.quickstart(create_app(config), '/', 'votes.conf')
    elif sys.argv[1] == 'initialise-database':
        app.drop_tables()
        app.create_tables()
    elif sys.argv[1] == 'dump-db':
        with open(sys.argv[2], mode='w') as file:
            json.dump(app.dump_models(), file, sort_keys=True, indent=2)
    elif sys.argv[1] == 'load-db':
        with open(sys.argv[2], mode='r') as file:
            app.load_models(json.load(file))
    else:
        print("Unknown argument", sys.argv[1])
