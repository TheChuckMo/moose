from requests import Session
from urllib.parse import urljoin


class BaseUrlSession(Session):
    """A Session with a URL that all requests will use as a base.
    Let's start by looking at an example:

    original code came from requests_toolbelt: https://github.com/requests/toolbelt/blob/master/requests_toolbelt/sessions.py
    """

    base_url: str = None

    def __init__(self, base_url: str):
        if base_url:
            if not base_url.endswith('/'):
                base_url = f'{base_url}/'
            self.base_url = base_url

        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        return super(BaseUrlSession, self).request(method, self.create_url(url.lstrip('/')), *args, **kwargs)

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url)
