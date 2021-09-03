# Connect Object

- Connect Object will always return a JSON

## Create connect

```python
from moose.connect import AppConnect
cnt = AppConnect('https://smoawx.ohsu.edu', username='user', password='pass')
```

## HTTP GET

```python
cnt.get('/api/path')
```
::: moose.connect.AppConnect.get
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP PUT

```python
cnt.put('/api/path')
```
::: moose.connect.AppConnect.put
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP POST

```python
cnt.post('/api/path')
```
::: moose.connect.AppConnect.post
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## HTTP DELETE

```python
cnt.delete('/api/path')
```
::: moose.connect.AppConnect.delete
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## cache_cookies

```python
cnt.cache_cookies()
```
::: moose.connect.AppConnect.cache_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## update_cookies

```python
cnt.update_cookies()
```
::: moose.connect.AppConnect.update_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true

## reload_cookies

```python
cnt.reload_cookies()
```
::: moose.connect.AppConnect.reload_cookies
    handler: python
    rendering:
      heading_level: 3
      show_root_heading: true
      show_source: true
