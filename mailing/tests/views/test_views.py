from . import BaseViewTest


class TestRootView(BaseViewTest):
    def test_index(self):
        resp = self.app.get('/admin/')
        self.assertIn('<script', resp)
