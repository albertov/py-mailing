from unittest2 import TestCase
from webtest import TestApp

class BaseViewTest(TestCase):
    def setUp(self):
        from dreamtellers.mailing.web.run import app_factory
        app = app_factory({
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.echo': True
        })
        self.app = TestApp(app)


class TestRootView(BaseViewTest):
    def test_index(self):
        resp = self.app.get('/')
        self.assertIn('<script', resp)
