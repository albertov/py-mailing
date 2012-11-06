from . import BaseViewTest


class TestGroupViews(BaseViewTest):
    def test_create_a_good_one(self):
        data = dict(name='foo')
        resp = self.app.post_json('/group/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['groups']), 1)
        item = resp.json['groups'][0]
        for k in data:
            self.assertEqual(item[k], data[k])

    def test_show_one(self):
        ob = self._makeGroup(name='foo')
        self.session.add(ob)
        self.session.flush()
        resp = self.app.get('/group/%s'%ob.id)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['groups']), 1)
        item = resp.json['groups'][0]
        self.assertEqual(item, ob.__json__())

    def test_list_collection(self):
        ob = self._makeGroup(name='foo')
        self.session.add(ob)
        self.session.flush()
        resp = self.app.get('/group/')
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['groups']), 1)
        item = resp.json['groups'][0]
        self.assertEqual(item, ob.__json__())

    def test_update_a_good_one(self):
        ob = self._makeGroup(name='foo')
        self.session.add(ob)
        self.session.flush()
        data = dict(ob.__json__(), name='bar')
        resp = self.app.put_json('/group/%s'%ob.id, data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['groups']), 1)
        item = resp.json['groups'][0]
        for k in data:
            self.assertEqual(item[k], data[k])
