from . import BaseViewTest

class TestMailingByNumber(BaseViewTest):
    def test_when_it_exists(self):
        m = self._makeMailing(number=0)
        tpl = self._makeTemplate(
            title='default',
            body='<html><body>${mailing.number}</body></html>')
        m.templates['xhtml'] = tpl
        self.session.add(m)
        self.session.flush()
        resp = self.app.get('/m/0/')
        self.assertIn('<html><body>0</body></html>', resp)

    def test_when_it_doesnt_exist(self):
        self.app.get('/m/0/', status=404)
