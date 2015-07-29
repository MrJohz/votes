from votes import quiz
import pytest


class TestQuiz:

    @pytest.fixture()
    def models(self, request, tmpdir):
        from votes import models
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

    def load_test_data(self, models):
        models.load_models(
            systems=[
                {'id': 0, 'name': 'system0', 'bite': '', 'data': ''},
                {'id': 1, 'name': 'system1', 'bite': '', 'data': ''},
                {'id': 2, 'name': 'system2', 'bite': '', 'data': ''},
                {'id': 3, 'name': 'system3', 'bite': '', 'data': ''}],
            questions=[
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
                        {'id': 5, 'systems': [1, 3], 'text': ''}]}],
            markdown=lambda x: x)

    def test_initialises_empty_components(self):
        q = quiz.Quiz(object())
        assert len(q.systems) == 0
        assert len(q.potential) == 0
        assert len(q.system_score) == 0
        assert len(q.system_order) == 0
        assert len(q.winners()) == 0

    def test_calculates_correctly(self, models):
        self.load_test_data(models)

        system0 = models.System.get(id=0)
        system1 = models.System.get(id=1)
        system2 = models.System.get(id=2)
        system3 = models.System.get(id=3)

        response = models.Response.create()
        response.answers.add(models.Answer.get(id=1))
        response.answers.add(models.Answer.get(id=2))

        # expected order: [3, (2, 0)]
        q = quiz.Quiz(response).calculate()
        assert q[0] == (system3, quiz.Score(2, 2))
        assert {q[1], q[2]} == {(system2, quiz.Score(1, 2)), (system0, quiz.Score(1, 2))}

    def test_calculates_winners(self, models):
        self.load_test_data(models)

        system0 = models.System.get(id=0)
        system1 = models.System.get(id=1)
        system2 = models.System.get(id=2)
        system3 = models.System.get(id=3)

        response = models.Response.create()
        response.answers.add(models.Answer.get(id=1))
        response.answers.add(models.Answer.get(id=2))

        q = quiz.Quiz(response).calculate()
        assert q.winners() == [system3]

        response = models.Response.create()
        response.answers.add(models.Answer.get(id=1))
        response.answers.add(models.Answer.get(id=3))
        response.answers.add(models.Answer.get(id=5))

        q = quiz.Quiz(response).calculate()
        assert set(q.winners()) == {system1, system2, system3}

    def test_getitem(self, models):
        self.load_test_data(models)

        system0 = models.System.get(id=0)
        system1 = models.System.get(id=1)
        system2 = models.System.get(id=2)
        system3 = models.System.get(id=3)

        response = models.Response.create()
        response.answers.add(models.Answer.get(id=1))
        response.answers.add(models.Answer.get(id=2))

        q = quiz.Quiz(response).calculate()
        assert q[0] == (system3, quiz.Score(2, 2))
        assert q[system3] == (system3, quiz.Score(2, 2))
