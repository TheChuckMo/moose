"""MooseTools connect headers"""
from typing import Mapping

json_content_accept: Mapping = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
"""Content-Type and accept headers for json"""

"""Content-Type headers"""
json_content: Mapping = {'Content-Type': 'application/json'}
form_urlencoded_content: Mapping = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

"""Accept headers"""
json_accept: Mapping = {'Accept': 'application/json'}
text_accept: Mapping = {'Accept': 'text/plain'}
html_accept: Mapping = {'Accept': 'text/html'}
xml_accept: Mapping = {'Accept': 'application/xml'}


"""header for Atlassian to not check token"""
no_check_atlassian_token: Mapping = {'X-Atlassian-Token': 'no-check'}
