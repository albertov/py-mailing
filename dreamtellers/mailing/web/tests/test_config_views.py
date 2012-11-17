from . import BaseViewTest


class TestConfigViews(BaseViewTest):
    def test_get_config(self):
        resp = self.app.get('/config')
        self.assertEqual(resp.json, {})

    def test_update_config(self):
        data = dict(foo='bar', zoo=3, car=True)
        resp = self.app.put_json('/config', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(resp.json['config'], data)
