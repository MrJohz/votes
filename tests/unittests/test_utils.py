from votes import utils


class TestQuickEnum:

    def test_has_correct_attributes(self):
        enum = utils.QuickEnum(name="name", seven=9)
        assert enum.name == "name"
        assert enum.seven == 9


class TestDewidow:

    def test_long_string(self):
        s = "this string has more than three words in it"
        assert utils.dewidow(s) == "this string has more than three words in&nbsp;it"

    def test_short_string(self):
        for i in ['short string', 'short', 'short string again']:
            assert utils.dewidow(i) == i

    def test_forced(self):
        s = "this string has many words in it"
        assert utils.dewidow(s, force=True) == "this string has many words in&nbsp;it"

        s = "short string"
        assert utils.dewidow(s, force=True) == "short&nbsp;string"

        s = "oneword"
        assert utils.dewidow(s, force=True) == "oneword"

        s = "short string again"
        assert utils.dewidow(s, force=True) == "short string&nbsp;again"

    def test_multiple(self):
        s = "this string has already been&nbsp;dewidowed"
        assert utils.dewidow(s) == s


class TestDestr:

    def test_with_string(self):
        assert utils.destr('hello') == ['hello']

    def test_with_list(self):
        assert utils.destr(['1', '2']) == ['1', '2']

    def test_with_none(self):
        assert utils.destr(None) == []
