# Chuck's Moose Tools

## [Connect](connect/index.md)

A generic connection object that always returns json for interacting with an API.

```python
from moosetools.connect import connect_json_app
cnt = connect_json_app('https://smoawx.ohsu.edu', username='user', password='pass')
```
