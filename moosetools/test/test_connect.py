import pytest
import os

from moosetools.connect import AppConnect, headers, _default_store_, _default_headers_


@pytest.fixture
def apidata():
    return {
        "connect": {
            "base_url": "https://api.dictionaryapi.dev/api/v2/",
            "auth": None,
            "headers": headers.json_content_accept,
            "store": _default_store_
        }
    }


@pytest.fixture
def connect(apidata):
    return AppConnect(**apidata['connect'])


def test_AppConnect(connect, apidata):
    assert connect.base_url == apidata['connect']['base_url']
    assert connect.headers == apidata['connect']['headers']
    assert connect.store == apidata['connect']['store']
    assert connect.cookie_store == os.path.join(connect.store, '.cookies')


def test_AppConnect_get(connect):
    monkey = connect.get('entries/en/monkey')
    assert monkey.ok is True
    assert monkey.status_code == 200

    monkey = connect.get('/entries/en/monkey')
    assert monkey.ok is True
    assert monkey.status_code == 200
