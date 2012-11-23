from webtest import TestApp

from ...tests.models import BaseModelTest

class BaseViewTest(BaseModelTest):
    def setUp(self):
        super(BaseViewTest, self).setUp()
        from ... import app_factory
        app = app_factory({'engine': self.engine})
        self.app = TestApp(app)