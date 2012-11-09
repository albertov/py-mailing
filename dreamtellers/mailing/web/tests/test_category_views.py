from . import BaseViewTest


class TestCategoryViews(BaseViewTest):
    def test_create_a_good_one(self):
        data = dict(title='foo', image_id=None, category_id=None)
        resp = self.app.post_json('/category/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['categories']), 1)
        item = resp.json['categories'][0]
        for k in data:
            self.assertEqual(item[k], data[k])

    def test_show_one(self):
        cat = self._makeCategory(title='foo')
        self.session.add(cat)
        self.session.flush()
        resp = self.app.get('/category/%s'%cat.id)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['categories']), 1)
        item = resp.json['categories'][0]
        self.assertEqual(item, cat.__json__())

    def test_list_collection(self):
        cat = self._makeCategory(title='foo')
        self.session.add(cat)
        self.session.flush()
        resp = self.app.get('/category/')
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['categories']), 1)
        item = resp.json['categories'][0]
        self.assertEqual(item, cat.__json__())

    def test_update_a_good_one(self):
        cat = self._makeCategory(title='foo')
        self.session.add(cat)
        self.session.flush()
        data = dict(cat.__json__(), title='bar')
        resp = self.app.put_json('/category/%s'%cat.id, data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['categories']), 1)
        item = resp.json['categories'][0]
        for k in data:
            self.assertEqual(item[k], data[k])
