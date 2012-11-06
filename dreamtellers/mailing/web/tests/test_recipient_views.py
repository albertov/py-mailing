from . import BaseViewTest


class TestRecipientViews(BaseViewTest):
    def test_create_a_good_one(self):
        data = dict(name='foo', email='foo@example.com')
        resp = self.app.post_json('/recipient/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['recipients']), 1)
        item = resp.json['recipients'][0]
        for k in data:
            self.assertEqual(item[k], data[k])

    def test_show_one(self):
        ob = self._makeRecipient(name='foo', email='foo@example.com')
        self.session.add(ob)
        self.session.flush()
        resp = self.app.get('/recipient/%s'%ob.id)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['recipients']), 1)
        item = resp.json['recipients'][0]
        self.assertEqual(item, ob.__json__())

    def test_list_collection(self):
        ob = self._makeRecipient(name='foo', email='foo@example.com')
        self.session.add(ob)
        self.session.flush()
        resp = self.app.get('/recipient/')
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['recipients']), 1)
        item = resp.json['recipients'][0]
        self.assertEqual(item, ob.__json__())

    def test_update_a_good_one(self):
        ob = self._makeRecipient(name='foo', email='foo@example.com')
        self.session.add(ob)
        self.session.flush()
        data = dict(ob.__json__(), name='bar')
        resp = self.app.put_json('/recipient/%s'%ob.id, data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['recipients']), 1)
        item = resp.json['recipients'][0]
        for k in data:
            self.assertEqual(item[k], data[k])
