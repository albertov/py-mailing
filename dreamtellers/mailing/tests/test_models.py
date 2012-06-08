import datetime
from unittest import TestCase


class BaseModelTest(TestCase):

    def setUp(self):
        self.session = self._makeSession()

    def _makeSession(self):
        from ..models import create_sessionmaker
        return create_sessionmaker()()

    def _makeMailing(self, **kw):
        from ..models import Mailing
        kw.setdefault('date', datetime.datetime(2010,1,1))
        return Mailing(**kw)

    def _makeExternalLink(self, **kw):
        from ..models import ExternalLink
        return ExternalLink(**kw)

    def _makeArticle(self, **kw):
        from ..models import Article
        return Article(**kw)

    def _makeImage(self, **kw):
        from ..models import Image
        return Image(**kw)

    def _makeCategory(self, **kw):
        from ..models import Category
        kw.setdefault('title', 'CategoryTitle')
        return Category(**kw)

class TestMailing(BaseModelTest):
    _makeOne = BaseModelTest._makeMailing

    def test_create(self):
        self.failUnless(self._makeOne())

    def test_create_persist_retrieve(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()
        self.failUnlessEqual(self.session.query(ob.__class__).count(), 1)


    def test_polymorphic_items(self):
        cat = self._makeCategory()
        item1 = self._makeExternalLink(title="Foo1", url="someurl", category=cat)
        item2 = self._makeArticle(title="Foo2", text="sometext", category=cat)
        ob = self._makeOne(items=[item2, item1])
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        items = retrieved.items
        self.failUnlessEqual(len(items), 2)
        self.failUnlessEqual(items[0].__class__.__name__, 'Article')
        self.failUnlessEqual(items[0].text, 'sometext')
        self.failUnlessEqual(items[1].__class__.__name__, 'ExternalLink')
        self.failUnlessEqual(items[1].url, 'someurl')

    def test_reverse_items(self):
        cat = self._makeCategory()
        item1 = self._makeArticle(title="Foo1", text="sometext", category=cat)
        item2 = self._makeArticle(title="Foo2", text="sometext", category=cat)
        ob = self._makeOne(items=[item1, item2])
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        retrieved.items[:] = retrieved.items[::-1]
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        items = retrieved.items
        self.failUnlessEqual(len(items), 2)
        self.failUnlessEqual(items[0].title, "Foo2")
        self.failUnlessEqual(items[1].title, "Foo1")
