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


if __name__ == '__main__':
    unittest.main()
