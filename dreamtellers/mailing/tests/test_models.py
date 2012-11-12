import datetime
from unittest2 import TestCase


class BaseModelTest(TestCase):

    def setUp(self):
        from ..models import Session, metadata, create_engine
        self.engine = create_engine('sqlite://')
        metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session

    def tearDown(self):
        self.session.remove()

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

    def _makeTemplate(self, **kw):
        from ..models import Template
        return Template(**kw)

    def _makeCategory(self, **kw):
        from ..models import Category
        kw.setdefault('title', 'CategoryTitle')
        return Category(**kw)

    def _makeGroup(self, **kw):
        from ..models import Group
        return Group(**kw)

    def _makeRecipient(self, **kw):
        from ..models import Recipient
        return Recipient(**kw)

    def _makeSentMailing(self, **kw):
        from ..models import SentMailing
        return SentMailing(**kw)



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
        item2 = self._makeArticle(title="Foo2", content="somecontent", category=cat)
        ob = self._makeOne(items=[item2, item1])
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        items = retrieved.items
        self.failUnlessEqual(len(items), 2)
        self.failUnlessEqual(items[0].__class__.__name__, 'Article')
        self.failUnlessEqual(items[0].content, 'somecontent')
        self.failUnlessEqual(items[1].__class__.__name__, 'ExternalLink')
        self.failUnlessEqual(items[1].url, 'someurl')

    def test_reverse_items(self):
        cat = self._makeCategory()
        item1 = self._makeArticle(title="Foo1", content="somecontent", category=cat)
        item2 = self._makeArticle(title="Foo2", content="somecontent", category=cat)
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

    def test_templates_descriptor(self):
        ob = self._makeOne()
        tpl = self._makeTemplate(title="fooo", body='foo')
        TYPE = 'xhtml'
        ob.templates[TYPE] = tpl
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(retrieved.templates[TYPE].type, TYPE)

class TestSentMailing(BaseModelTest):
    _makeOne = BaseModelTest._makeSentMailing

    def test_create(self):
        programmed_date = datetime.datetime(2010,1,1)
        ob = self._makeOne(mailing=self._makeMailing(),
                           programmed_date=programmed_date)
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(programmed_date, retrieved.programmed_date)

    def test_recipients(self):
        programmed_date = datetime.datetime(2010,1,1)
        ob = self._makeOne(mailing=self._makeMailing(),
                           programmed_date=programmed_date)
        ob.groups = [
            self._makeGroup(
                name = 'group_a',
                priority=1,
                recipients=[self._makeRecipient(name='foo',
                                                email='a@example.com'),
                            self._makeRecipient(name='bar',
                                                email='b@example.com')]),
            self._makeGroup(
                name = 'group_b',
                priority=0,
                recipients=[self._makeRecipient(name='foo2',
                                                email='a2@example.com'),
                            self._makeRecipient(name='bar2',
                                                email='b2@example.com')]),
        ]
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(2, len(retrieved.groups))
        self.failUnlessEqual(4, len(retrieved.recipients))
        from ..models import Recipient
        for r in retrieved.recipients:
            self.assertIsInstance(r, Recipient)
        names = [r.name for r in retrieved.recipients]
        self.failUnless(names.index('foo2')<names.index('foo'))
