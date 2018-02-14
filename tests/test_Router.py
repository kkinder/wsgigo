import unittest


class TestWsgiApp:
    def __init__(self, content_to_send="Hello, World"):
        self.content_to_send = content_to_send

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [self.content_to_send.encode('utf8')]


class TestRouter(unittest.TestCase):
    def test_host_route(self):
        from wsgigo import AppRouter

        app1 = TestWsgiApp('First app')
        app2 = TestWsgiApp('Second app')
        app3 = TestWsgiApp('Third')

        router = AppRouter(app1)
        router.add_hostname(app2, 'test1.local')
        router.add_hostname(app3, 'test2.local')

        self.assertEqual(router.get_route_app({'HTTP_HOST': 'foobar', 'PATH_INFO': '/'}), app1)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'test1.local', 'PATH_INFO': '/'}), app2)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'test2.local', 'PATH_INFO': '/'}), app3)

    def test_startswith_route(self):
        from wsgigo import AppRouter

        app1 = TestWsgiApp('First app')
        app2 = TestWsgiApp('Second app')
        app3 = TestWsgiApp('Third')

        router = AppRouter(app1)
        router.add_startswith(app2, '/foobar/')
        router.add_startswith(app3, '/spam/')

        self.assertEqual(router.get_route_app({'HTTP_HOST': 'localhost', 'PATH_INFO': '/'}), app1)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'localhost', 'PATH_INFO': '/monkey/'}), app1)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'localhost', 'PATH_INFO': '/foobar/cheese'}), app2)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'localhost', 'PATH_INFO': '/foobar/'}), app2)
        self.assertEqual(router.get_route_app({'HTTP_HOST': 'localhost', 'PATH_INFO': '/spam/'}), app3)

    def test_custom_router(self):
        from wsgigo import AppRouter, Route

        class InternetExplorerRouter(Route):
            def claim(self, environ):
                user_agent = environ['HTTP_USER_AGENT']
                if 'Trident/7.0' in user_agent or 'MSIE' in user_agent:
                    return True

        internet_explorer_app = TestWsgiApp("<b>really simple webpage</b>")
        real_app = TestWsgiApp("<b>really ADVANCED webpage</b>")

        router = AppRouter(default_app=real_app)
        router.add_route(InternetExplorerRouter(internet_explorer_app))

        self.assertEqual(router.get_route_app(
            {'HTTP_HOST': 'localhost',
             'PATH_INFO': '/',
             'HTTP_USER_AGENT': 'Lynx/2.8.1pre.9 libwww-FM/2.14'}),
            real_app)
        self.assertEqual(router.get_route_app(
            {'HTTP_HOST': 'localhost',
             'PATH_INFO': '/',
             'HTTP_USER_AGENT': 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}),
            internet_explorer_app)


if __name__ == '__main__':
    unittest.main()
