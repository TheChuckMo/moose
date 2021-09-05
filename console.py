import os

from moosetools.connect import AppConnect, json_headers

connect_dict = {
    "base_url": "https://api.dictionaryapi.dev/api/v2",
    "username": None,
    "password": None,
    "headers": None,
    "store": None
}

cnt = AppConnect(**connect_dict)

