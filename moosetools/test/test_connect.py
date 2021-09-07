import os

import pytest

from moosetools.connect import connect_json_app, _default_store_, __app__

# https://wordsapiv1.p.mashape.com/

free_dictionary_api_connect_string = {
    "base_url": "https://api.dictionaryapi.dev/api/v2/"
}
words_api_connect_string = {
    "base_url": "https://wordsapiv1.p.rapidapi.com/words/",
    "session_headers": {
        'x-rapidapi-host': os.getenv('moosetools_x_rapidapi_host'),
        'x-rapidapi-key': os.getenv('moosetools_x_rapidapi_key')
    }}

gorest_api_connect_string = {
    "base_url": "https://gorest.co.in/public/v1/",
    "session_headers": {'Authorization': f'Bearer {os.getenv("moosetools_gorest_token")}'},
    "session_keys": []
}

scenarios = {
    'free_dictionary_api': {
        "connect": {"base_url": "https://api.dictionaryapi.dev/api/v2/"},
        "get": [
            {"url": 'entries/en/monkey'},
            {"url": '/entries/en/monkey'}
        ]
    },
    'words_api': {
        'connect': {
            "base_url": "https://wordsapiv1.p.rapidapi.com/words/",
            "session_headers": {
                'x-rapidapi-host': os.getenv('moosetools_x_rapidapi_host'),
                'x-rapidapi-key': os.getenv('moosetools_x_rapidapi_key')
            }
        },
        "get": [
            {"url": 'entries/en/monkey'},
            {"url": '/entries/en/monkey'}
        ]
    }
}


@pytest.fixture(params=scenarios.keys())
def scenario(request):
    return scenarios.get(request.param)


@pytest.fixture
def connect(scenario):
    return connect_json_app(**scenario['connect'])


def test_connect_json_app(connect, scenario):
    assert connect.base_url == scenario['connect']['base_url']
    assert connect.store == (scenario['connect']['store'] or _default_store_)
    assert connect.session_store == os.path.join(connect.store, f'.{__app__}.session')


def test_connect_json_app_get(connect, scenario):
    for api in scenario.get('get'):
        _resp = connect.get(**api)
        assert _resp.ok is True
        assert _resp.status_code == 200
