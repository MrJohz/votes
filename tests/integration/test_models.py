from votes import models
import pytest


class TestModels:

    @pytest.fixture()
    def models(self, request, tmpdir):
        from peewee import SqliteDatabase

        db = SqliteDatabase(':memory:')
        original_meta_databases = []
        for model in models.tables:
            original_meta_databases.append(model._meta.database)
            model._meta.database = db
        models.create_tables()

        def teardown():
            models.drop_tables()
            for i, model in enumerate(models.tables):
                model._meta.database = original_meta_databases[i]
        request.addfinalizer(teardown)

        return models

    def test_load_models_as_empty(self, models):
        data = {
            'systems': [
                {'id': 0, 'name': 'system0', 'bite': '', 'data': ''},
                {'id': 1, 'name': 'system1', 'bite': '', 'data': ''},
                {'id': 2, 'name': 'system2', 'bite': '', 'data': ''},
                {'id': 3, 'name': 'system3', 'bite': '', 'data': ''}],
            'questions': [
                {'id': 0, 'text': 'question0', 'desc': '',
                    'answers': [
                        {'id': 0, 'systems': [0, 1], 'text': ''},
                        {'id': 1, 'systems': [2, 3], 'text': ''}]},
                {'id': 1, 'text': 'question1', 'desc': '',
                    'answers': [
                        {'id': 2, 'systems': [0, 3], 'text': ''},
                        {'id': 3, 'systems': [1, 2], 'text': ''}]},
                {'id': 2, 'text': 'question2', 'desc': '',
                    'answers': [
                        {'id': 4, 'systems': [0, 2], 'text': ''},
                        {'id': 5, 'systems': [1, 3], 'text': ''}]}]
        }
        models.load_models(markdown=lambda x: x, **data)

        assert models.System.select().count() == 4
        assert models.Question.select().count() == 3
        assert models.Answer.select().count() == 6

        for question in models.Question.select():
            assert question.answers.count() == 2
            for answer in question.answers:
                assert answer.systems.count() == 2

    def test_load_models_updating_db(self, models):
        data = {
            'systems': [
                {'id': 0, 'name': 'system0', 'bite': '', 'data': ''},
                {'id': 1, 'name': 'system1', 'bite': '', 'data': ''},
                {'id': 2, 'name': 'system2', 'bite': '', 'data': ''},
                {'id': 3, 'name': 'system3', 'bite': '', 'data': ''}],
            'questions': [
                {'id': 0, 'text': 'question0', 'desc': '',
                    'answers': [
                        {'id': 0, 'systems': [0, 1], 'text': ''},
                        {'id': 1, 'systems': [2, 3], 'text': ''}]},
                {'id': 1, 'text': 'question1', 'desc': '',
                    'answers': [
                        {'id': 2, 'systems': [0, 3], 'text': ''},
                        {'id': 3, 'systems': [1, 2], 'text': ''}]},
                {'id': 2, 'text': 'question2', 'desc': '',
                    'answers': [
                        {'id': 4, 'systems': [0, 2], 'text': ''},
                        {'id': 5, 'systems': [1, 3], 'text': ''}]}]
        }
        models.load_models(markdown=lambda x: x, **data)

        data = {
            'systems': [
                {'id': 0, 'name': 'system0', 'bite': 'bite-changed', 'data': ''}],
            'questions': [
                {'id': 0, 'text': 'question0', 'desc': '',
                    'answers': [
                        {'id': 0, 'systems': [0, 2], 'text': ''},
                        {'id': 1, 'systems': [1, 3], 'text': ''}]},
                {'id': 1, 'text': 'question1', 'desc': '',
                    'answers': [
                        {'id': 2, 'systems': [0, 3], 'text': ''},
                        {'id': 3, 'systems': [1, 2], 'text': ''}]},
                {'id': 2, 'text': 'question2', 'desc': '',
                    'answers': [
                        {'id': 4, 'systems': [0, 2], 'text': ''},
                        {'id': 5, 'systems': [1, 3], 'text': ''}]}]
        }
        models.load_models(markdown=lambda x: x, **data)

        assert models.System.get(id=0).bite == 'bite-changed'
        assert set(models.Answer.get(id=1).systems) == \
            {models.System.get(id=1), models.System.get(id=3)}

    def test_dump_models(self, models):
        data = {
            'systems': [
                {'id': 0, 'name': 'system0', 'bite': '', 'data': ''},
                {'id': 1, 'name': 'system1', 'bite': '', 'data': ''},
                {'id': 2, 'name': 'system2', 'bite': '', 'data': ''},
                {'id': 3, 'name': 'system3', 'bite': '', 'data': ''}],
            'questions': [
                {'id': 0, 'text': 'question0', 'desc': '',
                    'answers': [
                        {'id': 0, 'systems': [0, 1], 'text': ''},
                        {'id': 1, 'systems': [2, 3], 'text': ''}]},
                {'id': 1, 'text': 'question1', 'desc': '',
                    'answers': [
                        {'id': 2, 'systems': [0, 3], 'text': ''},
                        {'id': 3, 'systems': [1, 2], 'text': ''}]},
                {'id': 2, 'text': 'question2', 'desc': '',
                    'answers': [
                        {'id': 4, 'systems': [0, 2], 'text': ''},
                        {'id': 5, 'systems': [1, 3], 'text': ''}]}]
        }
        models.load_models(
            systems=data['systems'],
            questions=data['questions'],
            markdown=lambda x: x)

        systems, questions = models.dump_models()
        assert systems == data['systems']
        assert questions == data['questions']
