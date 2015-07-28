from configparser import ConfigParser
import cherrypy
from votes import VoteApplication, components

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
    elif sys.argv[1] == 'initialise-database':
        app.drop_tables()
        app.create_tables()
    elif sys.argv[1] == 'dump-db':
        with open(sys.argv[2], mode='w') as file:
            app.dump_models(file)
    elif sys.argv[1] == 'load-db':
        with open(sys.argv[2], mode='r') as file:
            app.load_models(file)
    else:
        print("Unknown argument", sys.argv[1])
