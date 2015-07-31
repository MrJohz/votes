from functional_helpers import FunctionalTestCase

import requests


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
                    {'id': 5, 'systems': [1, 3], 'text': ''}]}]}

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
        first_url = browser.url

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

        assert browser.url != first_url
        urls = [first_url, browser.url]

        browser.visit('http://localhost:8080/quiz')
        browser.choose('0', '0')
        browser.choose('1', '2')
        browser.choose('2', '4')
        browser.find_by_css('#quiz-submit').click()
        assert browser.url.startswith('http://localhost:8080/results')
        assert 'system1' in browser.html
        assert 'system2' in browser.html
        assert 'system3' in browser.html
        assert 'system0' in browser.html

        assert browser.url not in urls

    def test_no_input_produces_system_page(self, browser):
        browser.visit('http://localhost:8080/quiz')
        browser.find_by_css('#quiz-submit').click()
        assert browser.url == 'http://localhost:8080/systems'

    def test_ignores_invalid_integers(self):
        r = requests.post('http://localhost:8080/quiz', data={'4': 'e'})
        assert r.url == 'http://localhost:8080/systems'
        r = requests.post('http://localhost:8080/quiz', data={'e': '4'})
        assert r.url == 'http://localhost:8080/systems'

    def test_ignores_question_code_doesnt_match_answer_code(self):
        r = requests.post('http://localhost:8080/quiz', data={'0': '5'})
        assert r.url == 'http://localhost:8080/systems'

    def test_ignores_invalid_answer_id(self):
        r = requests.post('http://localhost:8080/quiz', data={'0': '9'})
        assert r.url == 'http://localhost:8080/systems'
