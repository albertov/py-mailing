from . import BaseViewTest
from ...models import Item, Article, ExternalLink


class TestNewItem(BaseViewTest):
    def test_create_a_good_article(self):
        m = self._makeMailing()
        self.session.add(m)
        self.session.flush()
        data = dict(title='foo', type='Article', mailing_id=m.id,
                    content='content')
        resp = self.app.post_json('/item/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['items']), 1)
        item = resp.json['items'][0]
        for k in data:
            self.assertEqual(item[k], data[k])
        self.assertIsInstance(Item.query.one(), Article)

    def test_create_two_articles(self):
        m = self._makeMailing()
        self.session.add(m)
        self.session.flush()
        data = [
            dict(title='foo', type='Article', mailing_id=m.id, content='ct'),
            dict(title='bar', type='Article', mailing_id=m.id, content='ct'),
            ]
        resp = self.app.post_json('/item/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['items']), 2)
        for item, data in zip(resp.json['items'], data):
            for k in data:
                self.assertEqual(item[k], data[k])

class TestUpdateItem(BaseViewTest):
    def test_update_a_good_article(self):
        art = self._makeArticle(title='foo', content='content')
        art.mailing = self._makeMailing()
        self.session.add(art)
        self.session.flush()
        data = dict(art.__json__(), title='bar')
        resp = self.app.put_json('/item/%s'%art.id, data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['items']), 1)
        item = resp.json['items'][0]
        for k in data:
            self.assertEqual(item[k], data[k])

    def test_update_two_articles(self):
        m = self._makeMailing()
        articles = [
            self._makeArticle(title='foo', content='bar', mailing=m),
            self._makeArticle(title='foo2', content='bar2', mailing=m),
            ]
        map(self.session.add, articles)
        self.session.flush()
        data = [a.__json__() for a in articles]
        for d in data:
            d['title']+='updated'
        resp = self.app.put_json('/item/0', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['items']), 2)
        for item, data in zip(resp.json['items'], data):
            for k in data:
                self.assertEqual(item[k], data[k])