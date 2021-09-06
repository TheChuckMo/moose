"""moose connect"""

import os
import pickle

import requests
from requests_toolbelt import user_agent

from moosetools import __app__, __version__
from moosetools.connect.headers import json_content_accept as _default_headers_
from moosetools.connect.response import AppResponse
from moosetools.connect.sessions import BaseUrlSession

"""default directory to store cookies and other cache"""
_default_store_: os.path = os.getcwd()

"""user-agent for connection"""
_user_agent_header: dict = {'User-Agent': user_agent(__app__, __version__)}


class AppConnect:
    """App connection object.

    A wrapper for requests BaseUrlSession to hold Atlassian keys across command runs.

    """
    _base_url: str
    _auth: (str, dict) = None
    _headers: dict = _default_headers_
    _store: os.path = _default_store_
    _response: requests.Response = None
    _session: requests.session = None
    _cookies: dict = dict()

    def __init__(self, base_url: str, auth: str = None, headers: dict = _default_headers_,
                 store: os.path = _default_store_) -> None:
        self._base_url = base_url

        if auth is not None:
            self._auth = auth

        if store is not None:
            self._store = store

        if headers is not None:
            self._headers = headers

        self.reload_cookies()

    @property
    def base_url(self) -> str:
        """base_url baseUrl for connection"""
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self._base_url = base_url
        if self.session:
            self.session.base_url = base_url

    @property
    def auth(self) -> object:
        """basic authentication for requests"""
        return self._auth

    @auth.setter
    def auth(self, auth):
        self._auth = auth

    @property
    def headers(self) -> dict:
        """session headers"""
        return self._headers

    @headers.setter
    def headers(self, headers: dict):
        self._headers = headers

    @property
    def store(self) -> str:
        """store directory for cookies and other cache"""
        return self._store

    @store.setter
    def store(self, store: os.path):
        self._store = os.path.abspath(store)

    @property
    def cookie_store(self) -> str:
        """store location for cookies"""
        return os.path.join(self.store, '.cookies')

    @property
    def session(self) -> BaseUrlSession:
        """session object"""
        if not self._session:
            self._session = BaseUrlSession(base_url=self.base_url)
            self._session.headers.update(_user_agent_header)

        return self._session

    def get(self, api, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False,
            allow_redirects=True) -> AppResponse:
        """send http get request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.
        allow_redirects

        Returns
        -------
        AppResponse
        """
        url = api

        try:
            self._response = self.session.get(url, headers=headers, params=params, data=data,
                                              auth=self.auth if auth else None, allow_redirects=allow_redirects)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.response(self._response)

    def delete(self, api, headers: dict = None, params=None, auth: bool = False) -> AppResponse:
        """send http delete request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        auth:       bool(False) send BasicAuth.

        Returns
        -------
        AppResponse
        """
        url = api

        try:
            self._response = self.session.delete(url, headers=headers, params=params, auth=self.auth if auth else None)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.response(self._response)

    def post(self, api: str, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False,
             allow_redirects: bool = True) -> AppResponse:
        """send http post request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.
        allow_redirects

        Returns
        -------
        AppResponse
        """
        url = api

        try:
            self._response = self.session.post(url, headers=headers, params=params, data=data,
                                               auth=self.auth if auth else None, allow_redirects=allow_redirects)
            # self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        # except requests.exceptions.HTTPError as err:
        #     raise SystemExit(err)

        return self.response(self._response)

    def put(self, api: str, headers: dict = None, params: dict = None, data: dict = None,
            auth: bool = False) -> AppResponse:
        """send http put request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.

        Returns
        -------
        AppResponse
        """
        url = api

        try:
            self._response = self.session.put(url, headers=headers, params=params, data=data,
                                              auth=self.auth if auth else None)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.response(self._response)

    def response(self, response: requests) -> AppResponse:
        """Always return a json response.

        Parameters
        ----------
        response:    response object.

        Returns
        -------
        AppResponse
        """

        if response.ok:
            if response.cookies:
                self.session.cookies.update(response.cookies)
            self.cache_cookies()

        return AppResponse(response=response)

    def cache_cookies(self):
        """cache cookies to file."""
        if self.session.cookies:
            self._cookies = self.session.cookies
            with open(self.cookie_store, 'wb') as f:
                pickle.dump(self._cookies, f)

    def reload_cookies(self):
        """reload cookies from file."""
        if os.path.isfile(self.cookie_store):
            with open(self.cookie_store, 'rb') as f:
                self._cookies = pickle.load(f)
            self.update_cookies()

    def update_cookies(self, cookies: dict = None):
        """add cookie(s) to cookie jar.
        Parameters
        ----------
        cookies
        """
        self.session.cookies.update(self._cookies)
        self.cache_cookies()
