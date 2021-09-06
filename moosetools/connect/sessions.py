import os
import pickle

from moosetools import __app__, __version__
from requests import Session
from requests_toolbelt import user_agent
from urllib.parse import urljoin

"""default directory to store cookies and other cache"""
_default_store_: os.path = os.getcwd()
_default_cookies_ext_: str = '.cookies'

"""user-agent for connection"""
_user_agent_header: dict = {'User-Agent': user_agent(__app__, __version__)}


class AppSession(Session):
    """A Session with a URL that all requests will use as a base.
    Let's start by looking at an example:

    original code came from requests_toolbelt: https://github.com/requests/toolbelt/blob/master/requests_toolbelt/sessions.py
    """

    base_url: str = None
    app: str = __name__
    store: os.path = os.getcwd()

    def __init__(self, base_url: str, app: str, store: os.path = None, *args, **kwargs):
        if base_url:
            if not base_url.endswith('/'):
                base_url = f'{base_url}/'
            self.base_url = base_url

        if app:
            self.app = app

        if store is not None:
            self.store = store

        super(AppSession, self).__init__(*args, **kwargs)

        self.reload_cookies()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.create_url(url)
        return super(AppSession, self).request(method, url, *args, **kwargs)

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url.lstrip('/'))

    @property
    def cookie_store(self) -> str:
        """store location for cookies"""
        return os.path.join(self.store, f'.{self.app}{_default_cookies_ext_}')

    def cache_cookies(self, session: Session):
        """cache cookies to file."""
        with open(self.cookie_store, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def reload_cookies(self):
        """reload cookies from file."""
        if os.path.isfile(self.cookie_store):
            with open(self.cookie_store, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
