import os

from moosetools.connect import connect_json
#
# gorest API
gorest_connect_string = {
    "base_url": "https://gorest.co.in/public/v1/",
    "token": f'{os.getenv("moosetools_gorest_api_token")}'
}
users = {
    "henry": {"name": "Henry The Eighth", "gender": "male", "email": "henry@eighth.com", "status": "active"}
}

gorest_ses = connect_json(**gorest_connect_string)

gorest_users = gorest_ses.get('/users')
print(f'{gorest_users.ok}')

gorest_users_paged = gorest_ses.get('/users', params={'page': '1'})
print(f'{gorest_users_paged.ok}')


#
# Words API connect
words_api_connect_string = {
    "base_url": "https://wordsapiv1.p.rapidapi.com/words/",
    "session_headers": {
        'x-rapidapi-host': os.getenv('moosetools_x_rapidapi_host'),
        'x-rapidapi-key': os.getenv('moosetools_x_rapidapi_key')
    }
}
# words_api_connect = connect_json(**words_api_connect_string)
# words_api_word1 = words_api_connect.get('incredible/definitions')
# print(words_api_word1.ok)
# words_api_word2 = words_api_connect.get('factory/synonyms')
# print(words_api_word2.ok)
# #
# # # Free dictionary connect
# free_dictionary_connect_string = {"base_url": "https://api.dictionaryapi.dev/api/v2/"}
# free_dictionary_connect = connect_json(**free_dictionary_connect_string)
# free_dictionary_word1 = free_dictionary_connect.get('entries/en/monkey')
# print(free_dictionary_word1.ok)
# free_dictionary_word2 = free_dictionary_connect.get('/entries/en/sponge')
# print(free_dictionary_word2.ok)
