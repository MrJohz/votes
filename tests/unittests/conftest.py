import pytest


@pytest.fixture
def data():
    return {
        'systems': ['sys1', 'sys2', 'sys3'],
        'questions': {
            'systems1&2': {
                'answers': {
                    'a1': {'systems': ['sys1', 'sys2']},
                    'a2': {'systems': ['sys3']}
                }
            },
            'system3': {
                'answers': {
                    'a1': {'systems': ['sys3']},
                    'a2': {'systems': ['sys1', 'sys2']}
                }
            },
            'systems2&3': {
                'answers': {
                    'a1': {'systems': ['sys2', 'sys3']},
                    'a2': {'systems': ['sys1']}
                }
            }
        }
    }
