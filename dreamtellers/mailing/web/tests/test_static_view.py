from . import BaseViewTest

class TestStaticFiles(BaseViewTest):
    def test_get_app_js(self):
        resp = self.app.get('/static/app.js')
        self.assertIn('Ext', resp)
