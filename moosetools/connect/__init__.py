"""MooseTools connect"""
import copy
import logging
from base64 import b64encode
from typing import Mapping, List, Any

from . import headers
from .sessions import AppSession

logger = logging.getLogger(__name__)


def connect_json(base_url: str, username: str = None, password: str = None, force_basic: bool = False,
                 session_cookies: Mapping = None, session_headers: Mapping = None, session_params: Mapping = None,
                 session_keys: List[Any] = None, store: str = None) -> AppSession:
    """create session with base_url of api server

    Parameters
    ----------
    base_url
    username
    password
    force_basic
    session_cookies
    session_headers
    session_params
    session_keys
    store

    Returns
    -------
    AppSession
    """
    _session = copy.deepcopy(AppSession)(base_url=base_url, store=store)

    update_session_headers(_session, headers=headers.json_content_accept)
    """update content-type and accept headers"""

    if (session_params is not None) and (len(session_params) > 0):
        _session.params.update(session_params)
        logger.debug(f'update session params: {session_params}')

    logger.info(f'init session params')

    if (session_headers is not None) and (len(session_headers) > 0):
        _session.headers.update(session_headers)
        logger.debug(f'update session headers: {session_headers}')

    logger.info(f'init session headers')

    if (session_cookies is not None) and (len(session_cookies) > 0):
        _session.cookies.update(session_cookies)
        logger.debug(f'update session cookies: {session_cookies}')

    logger.info(f'init session cookies')

    if session_keys:
        _session.session_keys = session_keys
        logger.info(f'session search keys: {session_keys}')

    logger.info(f'init session search keys')

    if username and password:
        set_session_basic_authentication(_session, force_basic=force_basic, username=username, password=password)

    return _session


def update_session_params(session: AppSession, params: Mapping) -> None:
    """add session params"""
    if (params is not None) and (len(params) > 0):
        session.params.update(params)
        logger.debug(f'add session params: {params}')


def update_session_cookies(session: AppSession, cookies: Mapping) -> None:
    """add session cookies"""
    if (cookies is not None) and (len(cookies) > 0):
        session.cookies.update(cookies)
        logger.debug(f'update session cookies: {cookies}')


def update_session_headers(session: AppSession, headers: Mapping) -> None:
    """add session headers"""
    if (headers is not None) and (len(headers) > 0):
        session.headers.update(headers)
        logger.debug(f'update session headers: {headers}')


def set_session_search_keys(session: AppSession, keys: List[Any]) -> None:
    """session search keys in headers or params to save"""
    if (keys is not None) and (type(keys) is list):
        session.session_keys = keys
        logger.info(f'session search keys: {session.session_keys}')


def set_session_basic_authentication(session: AppSession, username: str = None, password: str = None,
                                     force_basic: bool = False) -> None:
    """set basic authentication for session

    Parameters
    ----------
    session
    force_basic
    username
    password
    """
    if (username is not None) and (password is not None):
        session.auth = (username, password)
        logger.debug(f'basic auth for {username}')
        if force_basic:
            _basic_auth: bytes = b64encode(f'{username}:{password}'.encode())
            _basic_auth_header: Mapping = {'Authentication': f'Basic {_basic_auth}'.encode()}
            session.headers.update(_basic_auth_header)
            logger.debug(f'force basic auth for {username}')
