from votes import create_app
import cherrypy
import copy, tempfile, os


class FunctionalTestCase:

    default_config = {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()},
        'templating': {'directory': '"templates"'},
        'general': {'production': 'False', 'base_url': '"http://localhost:8080"'},
        'admin': {'username': '"admin"', 'password': '"test"', 'auth_key': '"auth_key_test"'}
    }

    _revertable_settings = {}

    @classmethod
    def setup_class(cls):
        cls._database_directory = tempfile.TemporaryDirectory(suffix='votes')
        cls._database_location = os.path.join(cls._database_directory.name, 'test.db')
        cls.default_config['database'] = {'file': '"' + cls._database_location + '"'}

        config = copy.deepcopy(cls.default_config)
        if hasattr(cls, 'config'):
            config.update(cls.config)

        app = create_app(config)
        app.create_tables()
        app.load_models(cls.database_input)
        cherrypy.tree.mount(app, '/', config)

        cls._revertable_settings['log.screen'] = cherrypy.log.screen
        cherrypy.log.screen = False

        cherrypy.engine.start()
        cls.app = app

    @classmethod
    def teardown_class(cls):
        cherrypy.engine.stop()
        cherrypy.engine.exit()

        cls.app.drop_tables()
        cherrypy.log.screen = cls._revertable_settings.get('log.screen', True)
