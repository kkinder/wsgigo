# WsgiGo

## What is it?

WSGI go is a very simple WSGI router with no requirements. It is written for Python 3, though it could be
easily backported.

## Installation

```
pip install wsgigo
```

## Usage

You can use it to route WSGI requests to specific apps based on hostname, URL fragment, or (through extending the
Route class) other criteria. For example, suppose you have three wsgi apps which you want to serve as one::

```python
from wsgigo import AppRouter

app = AppRouter(default_app=main_website)
app.add_startswith(docs_app, '/docs/')
app.add_hostname(api_app, 'api.local')
app.add_regexp(animal_app, '/(?:monkey|ape)/')
```

You can also make your own router class, to route apps how you need them to be routed::

```python
class InternetExplorerRouter(Route):
    def claim(self, environ):
        user_agent = environ['HTTP_USER_AGENT']
        if 'Trident/7.0' in user_agent or 'MSIE' in user_agent:
            return True

internet_explorer_app = TestWsgiApp("<b>really simple webpage</b>")
real_app = TestWsgiApp("<b>really ADVANCED webpage</b>")

router = AppRouter(default_app=real_app)
router.add_route(InternetExplorerRouter(internet_explorer_app))
```
