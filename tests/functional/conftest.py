import pytest


@pytest.fixture(scope='session')
def splinter_webdriver():
    return 'phantomjs'
