try:
    import json
except ImportError:
    import simplejson as json

import HTMLParser

from bottle import request

from webtest import TestApp

from ...tests.models import BaseModelTest

class BaseViewTest(BaseModelTest):
    _unescape = HTMLParser.HTMLParser().unescape

    def setUp(self):
        super(BaseViewTest, self).setUp()
        from ... import app_factory
        self._app = app_factory({'engine': self.engine})
        self.app = TestApp(self._app)

    def get_url(self, *args, **kw):
        try:
            request.bind({'SCRIPT_NAME':'/'})
            return self._app.get_url(*args, **kw)
        finally:
            del request.environ
            

    def json_from_html_body(self, body):
        return json.loads(self._unescape(body))
