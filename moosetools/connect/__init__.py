"""moose connect"""

import base64
import json
import os
import pickle
from json.decoder import JSONDecodeError

import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.sessions import BaseUrlSession

from moosetools.connect.headers import json_content_accept as _default_headers_

"""default directory to store cookies and other cache"""
_default_store_ = os.getcwd()


class AppResponse:
    response: requests.Response
    _json: dict = None

    def __init__(self, response: requests):
        self.response = response

    def __str__(self):
        self.json

    @property
    def ok(self):
        """status of response"""
        if self.response.ok:
            return self.response.ok

        return False

    @property
    def status_code(self):
        """the status code"""
        if self.response.status_code:
            return self.response.status_code

        return '000'

    @property
    def json(self):
        """Clean JSON object"""
        if not self._json:
            try:
                self._json = self.response.json()
            except JSONDecodeError as err:
                SystemExit(err)

        return json.dumps(self._json)


class AppConnect:
    """App connection object.

    A wrapper for requests BaseUrlSession to hold Atlassian keys across command runs.

    """
    _base_url: str
    _username: str
    _password: str
    _headers: _default_headers_
    _store: _default_store_
    _response: requests = None
    _session: requests = None

    def __init__(self, base_url: str, username: str = None, password: str = None, headers: dict = None,
                 store: str = None) -> None:
        self.base_url = base_url

        if username:
            self.username = username

        if password:
            self.password = password

        if store:
            self.store = store

        if headers:
            self.headers = headers

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
    def username(self) -> str:
        """username for connection"""
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def password(self) -> str:
        """password for connection."""
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    @property
    def auth(self) -> HTTPBasicAuth:
        """basic authentication for requests"""
        return HTTPBasicAuth(self.username, base64.decodebytes(self.password).decode())

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
        return os.path.abspath(self._store)

    @store.setter
    def store(self, store: str):
        self._store = store

    @property
    def cookie_store(self) -> str:
        """store location for cookies"""
        return os.path.join(self.store, '.cookies')

    @property
    def session(self) -> BaseUrlSession:
        """session object"""
        return BaseUrlSession(base_url=self.base_url)

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

    def update_cookies(self, cookies: dict = None):
        """add cookie(s) to cookie jar.

        Parameters
        ----------
        cookies
        """
        self.session.cookies.update(cookies)
        self.cache_cookies()

    def cache_cookies(self):
        """cache cookies to file."""
        if self.session.cookies:
            with open(self.cookie_store, 'wb') as f:
                pickle.dump(self.session.cookies, f)

    def reload_cookies(self):
        """reload cookies from file."""
        if os.path.isfile(self.cookie_store):
            with open(self.cookie_store, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
