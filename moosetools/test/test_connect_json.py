import os

import pytest
from typing import Dict, Any, List

from moosetools.connect import connect_json

test_users: Dict[str, Any] = {
    "henry": {"name": "Henry The Eighth", "gender": "male", "email": "henry@eighth.com", "status": "active"}
}

connect_string: Dict[str, Any] = {
    "base_url": "https://gorest.co.in/public/v1/",
    "token": f'{os.getenv("moosetools_gorest_api_token")}'
    #"session_headers": {'access-token': f'{os.getenv("moosetools_gorest_token")}'}
}

test_get_data: List[Any] = [
            pytest.param({"data": {'url': '/users'}}),
            pytest.param({"data": {'url': '/users', 'params': {'page': '1'}}}),
            pytest.param({"data": {'url': '/users/16'}}),
            pytest.param({"data": {'url': '/users/tommy'}}, marks=[pytest.mark.xfail(reason="no user")])
]

test_user_data: List[Any] = [
    pytest.param({'data': {'url': '/users', 'json': test_users.get("henry")}})
]


@pytest.fixture
def test_connect():
    _connect = connect_json(**connect_string)
    yield _connect
    _connect.close()


def test_connect_json(test_connect):
    assert test_connect.base_url == connect_string['base_url']


@pytest.mark.parametrize('test', test_get_data)
def test_connect_json_get(test_connect, test):
    print(test)
    _resp = test_connect.get(**test.get('data'))
    assert _resp.ok is True
    assert _resp.status_code == 200


@pytest.mark.parametrize('test', test_user_data)
def test_connect_json_user(test_connect, test):
    _res = test_connect.post(**test.get('data'))
    assert _res.ok is True
    assert _res.status_code == 201

    _user = _res.json().get('data')
    assert _user.get('name') == test_users.get("henry").get("name")
    assert _user.get('email') == test_users.get("henry").get("email")

    _del = test_connect.delete(f'/users/{_user.get("id")}')
    assert  _del.ok is True

