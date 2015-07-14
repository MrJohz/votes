from votes import quiz

import pytest

class TestQuiz(object):

    def test_quiz_determination(self, data):
        kind, winners, votes = quiz.determine(data, {'systems1&2': 'a1'})
        assert kind == quiz.PERFECT
        assert set(winners) == {'sys1', 'sys2'}

        kind, winners, votes = quiz.determine(data, {'systems1&2': 'a1', 'system3': 'a1'})
        assert kind == quiz.BEST
        assert set(winners) == {'sys1', 'sys2', 'sys3'}

    def test_quiz_failures(self, data):
        with pytest.raises(ValueError):
            quiz.determine(data, {})
