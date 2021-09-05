import pytest
import os

from moosetools.connect import AppConnect, json_headers, _default_store_


@pytest.fixture
def apidata():
    return {
        "connect": {
            "base_url": "https://ridb.recreation.gov/api/v1",
            "username": "user",
            "password": "pass",
            "headers": json_headers,
            "store": _default_store_,
        }
    }


@pytest.fixture
def connect(apidata):
    return AppConnect(**apidata['connect'])


def test_AppConnect(connect, apidata):
    assert connect.base_url == apidata['connect']['base_url']
    assert connect.username == apidata['connect']['username']
    assert connect.password != apidata['connect']['password']
    assert connect.headers == apidata['connect']['headers']
    assert connect.store == apidata['connect']['store']
    assert connect.cookie_store == os.path.join(connect.store, '.cookies')


def test_AppConnect_get(connect):
    assert connect.base_url == "https://ridb.recreation.gov/api/v1"
