from votes import create_app, models
import peewee
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
    def _setup_database(cls):
        db = peewee.SqliteDatabase(None)
        cls._original_meta_database = models.database
        models.database = db
        for model in models.tables:
            model._meta.database = db

    @classmethod
    def _teardown_database(cls):
        for i, model in enumerate(models.tables):
            model._meta.database = cls._original_meta_database
        models.database = cls._original_meta_database

    @classmethod
    def setup_class(cls):
        cls._database_directory = tempfile.TemporaryDirectory(suffix='votes')
        cls._database_location = os.path.join(cls._database_directory.name, 'test.db')

        config = copy.deepcopy(cls.default_config)
        config['database'] = {'file': '"' + cls._database_location + '"'}
        if hasattr(cls, 'config'):
            config.update(cls.config)

        cls._setup_database()

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
        cls._database_directory.cleanup()
        cls._database_directory = None
        cls._teardown_database()
