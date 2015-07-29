from functional_helpers import FunctionalTestCase


class TestStaticFiles(FunctionalTestCase):

    database_input = {
        'systems': [
            {'id': 0, 'name': 'system0', 'bite': 'system0-bite', 'data': 'sys0-data'},
            {'id': 1, 'name': 'system1', 'bite': 'system1-bite', 'data': 'sys1-data'},
            {'id': 2, 'name': 'system2', 'bite': 'system2-bite', 'data': 'sys2-data'},
            {'id': 3, 'name': 'system3', 'bite': 'system3-bite', 'data': 'sys3-data'}],
        'questions': [
            {'id': 0, 'text': 'question0', 'desc': 'question_0_description',
                'answers': [
                    {'id': 0, 'systems': [0, 1], 'text': ''},
                    {'id': 1, 'systems': [2, 3], 'text': ''}]},
            {'id': 1, 'text': 'question1', 'desc': 'question_1_description',
                'answers': [
                    {'id': 2, 'systems': [0, 3], 'text': ''},
                    {'id': 3, 'systems': [1, 2], 'text': ''}]},
            {'id': 2, 'text': 'question2', 'desc': 'question_2_description',
                'answers': [
                    {'id': 4, 'systems': [0, 2], 'text': ''},
                    {'id': 5, 'systems': [1, 3], 'text': ''}]}]
        }

    def test_quiz_submit(self, browser):
        browser.visit('http://localhost:8080/quiz')
        browser.choose('0', '1')
        browser.choose('1', '3')
        browser.choose('2', '5')
        browser.find_by_css('#quiz-submit').click()
        assert browser.url.startswith('http://localhost:8080/results')
        assert 'system1' in browser.html
        assert 'system2' in browser.html
        assert 'system3' in browser.html
        assert 'system0' not in browser.html
