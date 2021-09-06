import os

from moosetools.connect import AppConnect, headers

#_def_auth = HTTPBasicAuth(self.username, base63.decodebytes(self.password).decode())

connect_dict = {
    "base_url": "https://api.dictionaryapi.dev/api/v2",
    "auth": None,
    "headers": None,
    "store": None
}

free_dictionary_connect = {
    "base_url": "https://api.dictionaryapi.dev/api/v2/",
    "auth": None,
    "headers": headers.json_content_accept,
    "store": None
}

fdict = AppConnect(**free_dictionary_connect)

monkey = fdict.get('entries/en/monkey')
monkey2 = fdict.get('/entries/en/monkey')
#foass.get('/version')
