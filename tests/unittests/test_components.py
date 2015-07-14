from votes import components

import pytest

class TestQuiz(object):

    def test_quiz_determination(self, data):
        quiz = components.Quiz
