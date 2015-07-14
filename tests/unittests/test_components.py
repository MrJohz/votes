from votes import components

import pytest

class TestQuiz(object):

    def test_quiz_determination(self, data):
        quiz = components.Quiz(data=data)
        kind, winners, votes = quiz.determine({'systems1&2': 'a1'})
        assert kind == quiz.winner_kind.perfect
        assert set(winners) == {'sys1', 'sys2'}

        kind, winners, votes = quiz.determine({'systems1&2': 'a1', 'system3': 'a1'})
        assert kind == quiz.winner_kind.best
        assert set(winners) == {'sys1', 'sys2', 'sys3'}

    def test_quiz_failures(self, data):
        quiz = components.Quiz(data=data)
        with pytest.raises(ValueError):
            quiz.determine({})
