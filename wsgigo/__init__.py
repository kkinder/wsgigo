import typing


class Route:
    def __init__(self, app: callable):
        self.app = app

    def claim(self, environ):
        raise NotImplementedError


class StandardRoute(Route):
    def __init__(self, app: callable, startswith: str = None, hostname: str = None):
        super().__init__(app)

        self.startswith = startswith
        self.hostname = hostname

    def claim(self, environ):
        path = environ['PATH_INFO']
        host = environ['HTTP_HOST'].split(':')[0]

        if self.startswith:
            if path.startswith(self.startswith):
                return True
        if self.hostname:
            if host.lower() == self.hostname.lower():
                return True


class AppRouter:
    def __init__(self, default_app: callable, routes: typing.List[Route] = None):
        self.default_app = default_app
        self.routes = routes or []

    def add_route(self, route: Route):
        self.routes.append(route)

    def add_startswith(self, app, pattern):
        self.routes.append(StandardRoute(app, startswith=pattern))

    def add_hostname(self, app, hostname):
        self.routes.append(StandardRoute(app, hostname=hostname))

    def get_route_app(self, environ):
        for route in self.routes:
            if route.claim(environ):
                return route.app
        return self.default_app

    def __call__(self, environ, start_response):
        return self.get_route_app(environ)(environ, start_response)


__all__ = ['AppRouter', 'StandardRoute', 'Route']
