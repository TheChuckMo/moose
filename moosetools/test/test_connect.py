import pytest
import os

from moosetools.connect import connect_json_app, _default_store_, __app__
from moosetools.connect.sessions import _default_cookies_ext_


@pytest.fixture
def apidata():
    return {
        "connect": {
            "base_url": "https://api.dictionaryapi.dev/api/v2/",
            "username": None,
            "password": None,
            "store": _default_store_
        }
    }


@pytest.fixture
def connect(apidata):
    return connect_json_app(**apidata['connect'])


def test_AppConnect(connect, apidata):
    assert connect.base_url == apidata['connect']['base_url']
    assert connect.store == apidata['connect']['store']
    assert connect.cookie_store == os.path.join(connect.store, f'.{__app__}{_default_cookies_ext_}')


def test_AppConnect_get(connect):
    monkey = connect.get('entries/en/monkey')
    assert monkey.ok is True
    assert monkey.status_code == 200

    monkey = connect.get('/entries/en/monkey')
    assert monkey.ok is True
    assert monkey.status_code == 200
