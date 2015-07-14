from votes import components

import pytest

class TestQuiz(object):

    def test_quiz_determination(self, data):
        quiz = components.Quiz(data=data)
        kind, winners = quiz.determine({'sys1&2': 'a1'})
        assert kind == quiz.winner_kind.perfect
        assert set(winners) == {'sys1', 'sys2'}

