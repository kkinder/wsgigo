import typing
import re


class Route:
    def __init__(self, app: callable):
        self.app = app

    def claim(self, environ):
        raise NotImplementedError


class StandardRoute(Route):
    def __init__(self, app: callable, startswith: str = None, hostname: str = None, strip_startswith: bool = False):
        super().__init__(app)

        self.startswith = startswith
        self.hostname = hostname
        self.strip_startswith = strip_startswith

    def claim(self, environ):
        path = environ['PATH_INFO']
        host = environ['HTTP_HOST'].split(':')[0]

        if self.startswith:
            if path.startswith(self.startswith):
                if self.strip_startswith:
                    path = path[len(self.startswith):]
                    if not path.startswith('/'):
                        path = '/' + path
                    environ['PATH_INFO'] = path
                return True
        if self.hostname:
            if host.lower() == self.hostname.lower():
                return True


class RegExpRoute(Route):
    def __init__(self, app: callable, pattern):
        super().__init__(app)

        self.pattern = pattern

    def claim(self, environ):
        path = environ['PATH_INFO']

        match = self.pattern.match(path)
        if match:
            if match.groups():
                assert len(match.groups()) == 1, "multiple match groups not supported"
                path = match.group(1)
                if not path.startswith('/'):
                    path = '/' + path
                environ['PATH_INFO'] = path
            return True


class AppRouter:
    def __init__(self, default_app: callable, routes: typing.List[Route] = None):
        self.default_app = default_app
        self.routes = routes or []

    def add_route(self, route: Route):
        self.routes.append(route)

    def add_startswith(self, app, pattern, strip_startswith=False):
        self.routes.append(StandardRoute(app, startswith=pattern, strip_startswith=strip_startswith))

    def add_hostname(self, app, hostname):
        self.routes.append(StandardRoute(app, hostname=hostname))

    def add_regexp(self, app, pattern):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.routes.append(RegExpRoute(app, pattern))

    def get_route_app(self, environ):
        for route in self.routes:
            if route.claim(environ):
                return route.app
        return self.default_app

    def __call__(self, environ, start_response):
        return self.get_route_app(environ)(environ, start_response)


__all__ = ['AppRouter', 'StandardRoute', 'Route']
