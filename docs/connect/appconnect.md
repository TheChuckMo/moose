# Connect Object

- Connect Object will always return the response object with JSON

## Create connect

```python
from moosetools.connect import AppConnect
cnt = AppConnect('https://smoawx.ohsu.edu', username='user', password='pass')
```

## HTTP GET

```python
cnt.get('/api/path')
```
::: moosetools.connect.AppConnect.get
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP PUT

```python
cnt.put('/api/path')
```
::: moosetools.connect.AppConnect.put
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP POST

```python
cnt.post('/api/path')
```
::: moosetools.connect.AppConnect.post
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP DELETE

```python
cnt.delete('/api/path')
```
::: moosetools.connect.AppConnect.delete
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## cache_cookies

```python
cnt.cache_cookies()
```
::: moosetools.connect.AppConnect.cache_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## update_cookies

```python
cnt.update_cookies()
```
::: moosetools.connect.AppConnect.update_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## reload_cookies

```python
cnt.reload_cookies()
```
::: moosetools.connect.AppConnect.reload_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true
