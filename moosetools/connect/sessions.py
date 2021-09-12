"""MooseTools sessions"""

import json
import os
import pickle
import logging

from typing import List, Any, Mapping
from urllib.parse import urljoin, urlparse, parse_qsl

import requests
from requests import Session
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from requests_toolbelt import user_agent

from moosetools import __app__, __version__

logger = logging.getLogger(__name__)
"""the logger"""

_store_: str = os.getcwd()
"""default directory to session cache"""

_session_app_: str = __app__
"""default user agent for session"""

_session_app_version_: str = __version__
"""default user agent version for session"""

_session_keys_: List[str] = []
"""default session keys"""

_session_ext_: str = '.moose'
"""default extension for session cache file"""


class AppSession(Session):
    """Request session with base_url and caching of session"""

    base_url: str = ''
    app: str = _session_app_
    version: str = _session_app_version_
    store: str = _store_
    _session_keys: List[str] = _session_keys_

    def __init__(self, base_url: str, store: str = None, session_keys: List[str] = None) -> None:
        """init AppSession"""
        if base_url:
            if not base_url.endswith('/'):
                base_url = f'{base_url}/'
            self.base_url = base_url

        if store is not None:
            self.store = store

        if session_keys is not None:
            self.session_keys = session_keys

        super(AppSession, self).__init__()

        self.set_user_agent()
        """set user agent header to session"""

        self.hooks['response'].append(self._cache_session)
        """add cache_session hook to session"""

        self._reload_session()
        """reload cached session"""

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.build_url(url)
        return super(AppSession, self).request(method, url, *args, **kwargs)

    def build_url(self, url) -> str:
        """Build full url from base_url and api path"""
        return urljoin(self.base_url, url.lstrip('/'))

    @property
    def session_store(self) -> str:
        """store cache file for sessions"""
        return os.path.join(self.store, f'.{self.app}{_session_ext_}')

    @property
    def session_keys(self) -> list:
        """Session keys in headers and params"""
        return self._session_keys

    @session_keys.setter
    def session_keys(self, keys: list) -> None:
        """Set to unique list of session keys"""
        keys.append(self._session_keys)
        _used: List[Any] = []
        self._session_keys = [x for x in keys if x not in _used and (_used.append(x) or True)]

    def _cache_session(self, response: requests.Response) -> None:
        """Save session to cache file"""
        _session: Mapping = {'cookies': dict(), 'headers': dict(), 'params': dict()}

        logger.info(f'session keys: {self.session_keys}')

        _cookies: Mapping = dict_from_cookiejar(response.cookies)
        if len(_cookies) > 0:
            logger.debug(f'response cookies: {_cookies}')
            _session['cookies'].update({k: v for (k, v) in _cookies.items() if k in self.session_keys})

        _headers: Mapping = response.headers
        if len(_headers) > 0:
            logger.debug(f'response headers: {_headers}')
            _session['headers'].update({k: v for (k, v) in _headers.items() if k in self.session_keys})

        _query: str = urlparse(response.request.url).query
        _params: Mapping = dict(parse_qsl(_query))
        if len(_params) > 0:
            logger.debug(f'request params: {json.dumps(_params)}')
            _session['params'].update({k: v for (k, v) in _params.items() if k in self.session_keys})

        if _session:
            logger.info(f'write session cache: {json.dumps(_session)}')
            with open(self.session_store, 'wb') as f:
                pickle.dump(_session, f)

    def _reload_session(self) -> None:
        """reload session from cache file"""
        _session: Mapping = dict()
        if os.path.isfile(self.session_store):
            with open(self.session_store, 'rb') as f:
                _session = pickle.load(f)

        logger.info(f'read session cache: {_session}')
        if ('cookies' in _session) and (len(_session['cookies']) > 0):
            self.cookies = cookiejar_from_dict(_session.get('cookies'))
            logger.debug(f'reloaded cookies: {json.dumps(_session.get("cookies"))}')

        if ('headers' in _session) and (len(_session['headers']) > 0):
            self.headers = _session.get('headers')
            logger.debug(f'reloaded headers: {_session.get("headers")}')

        if ('params' in _session) and (len(_session['params']) > 0):
            self.params = _session.get('params')
            logger.debug(f'reloaded params: {_session.get("params")}')

    def set_user_agent(self, app: str = None, version: str = None) -> None:
        """set user-agent for connection"""
        if app is not None:
            self.app = app

        if version is not None:
            self.version = version

        self.headers.update({'User-Agent': user_agent(self.app, self.version)})
        logger.debug(f'set user agent {self.app} - {self.version}')

