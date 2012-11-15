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

class TestNewMailing(BaseViewTest):
    def test_create_a_good_one(self):
        tpl = self._makeTemplate(
            title='default',
            body='<html><body>${mailing.number}</body></html>')
        self.session.add(tpl)
        self.session.flush()
        data = dict(number=0, date='2010-01-01T00:00:00')
        resp = self.app.post_json('/mailing/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['mailings']), 1)
        item = resp.json['mailings'][0]
        self.assertEqual(item['date'], data['date'])
        self.assertEqual(item['number'], 1) #uses next_number()

    def test_no_default_template(self):
        data = dict(number=0, date='2010-01-01T00:00:00')
        resp = self.app.post_json('/mailing/', data, status=400)
        self.assertFalse(resp.json['success'])

    def test_create_a_bad_one(self):
        data = dict(number=0, date='2010-01-Z')
        resp = self.app.post_json('/mailing/', data, status=400)
        self.assertFalse(resp.json['success'])

class TestUpdateMailing(BaseViewTest):
    def test_update_a_good_one(self):
        tpl = self._makeTemplate(
            title='default',
            body='<html><body>${mailing.number}</body></html>')
        mailing = self._makeMailing(number=0)
        mailing.templates['xhtml'] = tpl
        self.session.add(mailing)
        self.session.flush()
        data = dict(mailing.__json__(), date='2010-01-01T00:00:00')
        resp = self.app.put_json('/mailing/%s'%mailing.id, data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['mailings']), 1)
        item = resp.json['mailings'][0]
        for k in data:
            if k!='modified':
                self.assertEqual(item[k], data[k])
