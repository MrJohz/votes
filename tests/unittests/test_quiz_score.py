from votes import quiz


class TestScore:

    def test_initialises_fraction(self):
        score = quiz.Score(4, 8)
        assert score.fraction == 0.5

    def test_keeps_numerator_and_denominator(self):
        score = quiz.Score(4, 8)
        assert score.numerator == 4
        assert score.denominator == 8

    def test_stringification(self):
        score = quiz.Score(4, 8)
        assert str(score) == "4/8"

    def test_equals(self):
        score_1 = quiz.Score(4, 8)
        score_2 = quiz.Score(2, 4)
        score_3 = quiz.Score(3, 8)
        score_4 = quiz.Score(4, 8)

        assert score_1 != score_2
        assert score_1 != score_3
        assert score_1 == score_4

    def test_hashable(self):
        score_1 = quiz.Score(4, 8)
        score_2 = quiz.Score(2, 4)
        score_3 = quiz.Score(3, 8)
        score_4 = quiz.Score(4, 8)

        score_set = {score_1}
        assert score_2 not in score_set
        assert score_3 not in score_set
        assert score_4 in score_set
