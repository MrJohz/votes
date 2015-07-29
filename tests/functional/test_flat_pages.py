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

    def assert_menu_exists(self, browser):
        for i in ('quiz', 'systems', 'about' ''):
            assert browser.find_link_by_href('http://localhost:8080/' + i)

    def test_main_page(self, browser):
        browser.visit('http://localhost:8080')
        self.assert_menu_exists(browser)

    def test_quiz_page(self, browser):
        browser.visit('http://localhost:8080/quiz')
        self.assert_menu_exists(browser)
        for question in self.database_input['questions']:
            assert question['text'] in browser.html
            assert question['desc'] in browser.html

    def test_systems_page(self, browser):
        browser.visit('http://localhost:8080/systems')
        self.assert_menu_exists(browser)
        for system in self.database_input['systems']:
            assert system['bite'] in browser.html
            assert browser.find_link_by_href('http://localhost:8080/systems/' + str(system['id']))

    def test_subsystems_page(self, browser):
        browser.visit('http://localhost:8080/systems/1')
        self.assert_menu_exists(browser)
        assert self.database_input['systems'][1]['name'] in browser.html
        assert self.database_input['systems'][1]['data'] in browser.html

    def test_about_page(self, browser):
        browser.visit('http://localhost:8080/about')
        self.assert_menu_exists(browser)


class TestErrorPages(FunctionalTestCase):

    def test_nonexistant_subsystems_page(self, browser):
        browser.visit('http://localhost:8080/systems/1392')
        assert browser.status_code == 404

    def test_nonexistant_results_page(self, browser):
        browser.visit('http://localhost:8080/results/anything_will_do_here')
        assert browser.status_code == 404
