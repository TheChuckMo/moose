import os

import pytest
from typing import Dict, Any, List

from moosetools.connect import connect_json
from moosetools.connect.sessions import _store_


connect_string: Dict[str, Any] = {
        "base_url": "https://gorest.co.in/public/v1/",
        "session_headers": {'Authorization': f'Bearer {os.getenv("moosetools_gorest_api_token")}'}
}

get_test_data: List[Any] = [
            pytest.param({"data": '/users'}),
            pytest.param({"data": {'url': '/users', 'params': {'page': '1'}}})
]

put_test_data: List[Any] = []
test_post_data: List[Any] = []
test_patch_data: List[Any] = []
test_delete_data: List[Any] = []


@pytest.fixture
def test_connect():
    _connect = connect_json(**connect_string)
    yield _connect
    _connect.close()


def test_connect_json(test_connect):
    assert test_connect.base_url == connect_string['base_url']

#
# @pytest.mark.parametrize('get_tests_data', scenarios, indirect=True)
# def test_app_session_get(connect, get_tests_data):
#     print(get_tests_data)
#     _resp = connect.get(*get_tests_data)
#     assert _resp.ok is True
#     assert _resp.status_code == 200
