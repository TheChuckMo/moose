"""moose connect"""

import os
from base64 import b64encode

from requests_toolbelt import user_agent

from moosetools import __app__, __version__
from moosetools.connect import headers
from moosetools.connect.sessions import AppSession

"""default directory to store cookies and other cache"""
_default_store_: os.path = os.getcwd()

"""user-agent for connection"""
_user_agent_header: dict = {'User-Agent': user_agent(__app__, __version__)}


class AppAuth:
    type: str = 'basic'
    username: str = None
    password: str = None


def connect_json_app(base_url: str, username: str = None, password: str = None, force_basic: bool = False,
                     apikey: (list, tuple) = None, store: os.path = _default_store_) -> AppSession:
    """create app session with base_url of api server

    Parameters
    ----------
    base_url
    username
    password
    force_basic
    apikey
    store

    Returns
    -------
    AppSession
    """
    _session = AppSession(base_url=base_url, app=__app__, store=store)

    """set user agent header"""
    _session.headers.update(_user_agent_header)

    """set json headers"""
    _session.headers.update(headers.json_content_accept)

    """add basic authentication to session"""
    if (username is not None) and (password is not None):
        _session.auth = (username, password)
        if force_basic:
            _basic_auth = b64encode(f'{username}:{password}')
            _session.headers.update({'Authentication': f'Basic {_basic_auth}'})

    if (apikey is not None) and (len(apikey) == 2):
        _session.headers.update({f'{apikey[0]}': f'{apikey[1]}'})

    return _session
