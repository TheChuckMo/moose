from moosetools.connect.sessions import AppSession, _session_ext_, _session_app_
from typing import List

base_url: str = 'https://example.com/api/v1'
app: str = 'gremlin'
version: str = '1.1.1'
store: str = '/tmp'
session_keys: List[str] = ['session', 'authorize']


def test_app_session_base_url():
    cnt = AppSession(base_url)
    assert cnt.base_url == f'{base_url}/'


def test_app_session_app():
    cnt = AppSession(base_url)
    assert cnt.app == _session_app_


def test_app_session_store():
    cnt = AppSession(base_url, store=store)
    assert cnt.session_store == f'{store}/.{_session_app_}{_session_ext_}'


def test_app_session_keys():
    cnt = AppSession(base_url, session_keys=session_keys)
    assert cnt.session_keys == session_keys


# def test_app_session_hooks():
#     cnt = AppSession(base_url, session_keys=session_keys)
#     assert len(cnt.hooks['response']) == 1


def test_app_session_user_agent():
    cnt = AppSession(base_url)
    cnt.set_user_agent(app=app, version=version)
    assert cnt.app == app
    assert cnt.version == version
    assert "User-Agent" in cnt.headers
