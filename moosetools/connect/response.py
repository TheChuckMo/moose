import json
from json import JSONDecodeError

import requests


class AppResponse:
    response: requests.Response
    mode: str = 'json'
    _json: dict = None

    def __init__(self, response: requests, mode: str = None):
        self.response = response

        if mode:
            self.mode = mode

            self._set_json()

    def __str__(self):
        return self.json

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

        return None

    def _set_json(self):
        """get json from response"""
        if self.mode is 'json':
            try:
                self._json = self.response.json()
            except JSONDecodeError as err:
                SystemExit(err)
        else:
            self._json = dict()

    @property
    def json(self):
        """Clean JSON object"""
        if not self._json:
            self._set_json()

        return json.dumps(self._json)
