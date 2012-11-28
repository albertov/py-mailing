import random
import datetime

from . import BaseModelTest


class TestMailing(BaseModelTest):
    _makeOne = BaseModelTest._makeMailing

    def test_create(self):
        self.failUnless(self._makeOne())

    def test_create_persist_retrieve(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.session.expunge_all()
        self.failUnlessEqual(self.session.query(ob.__class__).count(), 1)


    def test_polymorphic_items(self):
        cat = self._makeCategory()
        item1 = self._makeExternalLink(title="Foo1", url="someurl", category=cat)
        item2 = self._makeArticle(title="Foo2", content="somecontent", category=cat)
        ob = self._makeOne(items=[item2, item1])
        self.session.add(ob)
        self.session.flush()
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
        self.session.flush()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        retrieved.items[:] = retrieved.items[::-1]
        self.session.flush()
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
        self.session.flush()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(retrieved.templates[TYPE].type, TYPE)

class TestMailingDelivery(BaseModelTest):
    _makeOne = BaseModelTest._makeMailingDelivery

    def test_create(self):
        programmed_date = datetime.datetime(2010,1,1)
        ob = self._makeOne(mailing=self._makeMailing(),
                           programmed_date=programmed_date)
        self.session.add(ob)
        self.session.flush()
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
        self.session.flush()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(2, len(retrieved.groups))
        self.failUnlessEqual(4, len(retrieved.recipients))
        from ...models import Recipient
        for r in retrieved.recipients:
            self.assertIsInstance(r, Recipient)
        names = [r.name for r in retrieved.recipients]
        self.failUnless(names.index('foo2')<names.index('foo'))

        for g in retrieved.groups:
            self.session.delete(g)
        self.session.flush()
        self.session.expire(retrieved)
        self.failUnlessEqual(0, len(retrieved.groups))
        self.failUnlessEqual(0, len(retrieved.recipients))

    def test_processed_recipients(self):
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
        self.session.flush()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()
        self.failUnlessEqual(0, len(retrieved.processed_recipients))
        retrieved.processed_recipients.append(retrieved.groups[0].recipients[0])

        self.session.flush()
        self.session.expunge_all()

        retrieved = self.session.query(ob.__class__).one()

        self.failUnlessEqual(1, len(retrieved.processed_recipients))
        self.failUnlessEqual(3, len(retrieved.unprocessed_recipients))
        from ...models import Recipient
        for r in retrieved.processed_recipients:
            self.assertIsInstance(r, Recipient)

    def test_next_in_queue_none_programmed(self):
        ob = self._makeOne(mailing=self._makeMailing())
        self.session.add(ob)
        self.session.flush()
        self.session.expunge_all()

        d = datetime.datetime(2010,1,1,15)
        self.assertFalse(ob.__class__.next_in_queue(d))

    def test_next_in_queue_picks_one_with_lowest_programmed_date(self):
        ds = [datetime.datetime(2010,1,1,i+10) for i in xrange(5)]
        random.shuffle(ds)
        for i,d in enumerate(ds):
            ob = self._makeOne(mailing=self._makeMailing(number=i),
                               programmed_date=d)
            cls = ob.__class__
            self.session.add(ob)
        self.session.flush()
        self.session.expunge_all()

        d = max(ds) + datetime.timedelta(hours=1)
        next = cls.next_in_queue(d)
        self.assertEqual(min(ds), next.programmed_date)

    def test_next_in_queue_ignores_sent_ones(self):
        ds = [datetime.datetime(2010,1,1,i+10) for i in xrange(5)]
        random.shuffle(ds)
        for i,d in enumerate(ds):
            ob = self._makeOne(mailing=self._makeMailing(number=i),
                               programmed_date=d)
            cls = ob.__class__
            self.session.add(ob)
        self.session.flush()
        self.session.expunge_all()

        d = max(ds) + datetime.timedelta(hours=1)
        processed = set()
        for _ in xrange(len(ds)):
            next = cls.next_in_queue(d)
            self.assertFalse(next in processed)
            processed.add(next)
            self.assertIs(None, next.sent_date)
            next.sent_date = d
            self.session.flush()
        self.assertFalse(cls.next_in_queue(d))


class TestMailingDeliveryProcessedRecipient(BaseModelTest):

    def _makeOne(self, mailing_delivery=None, recipient=None):
        if mailing_delivery is None:
            mailing_delivery = self._makeMailingDelivery(
                mailing=self._makeMailing()
                )
        if recipient is None:
            recipient = self._makeRecipient()
        return self._makeMailingDeliveryProcessedRecipient(
            recipient=recipient, mailing_delivery=mailing_delivery)

    def test_delete_mailing_delivery_cascades(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.assertEqual(1, ob.__class__.query.count())
        self.session.delete(ob.mailing_delivery)
        self.session.flush()
        self.assertEqual(0, ob.__class__.query.count())

    def test_delete_recipient_cascades(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.assertEqual(1, ob.__class__.query.count())

        self.session.delete(ob.recipient)
        self.session.flush()
        self.assertEqual(0, ob.__class__.query.count())

    def test_uuid_is_hex(self):
        ob = self._makeOne()
        self.assertEqual(16, len(ob.uuid.decode('hex')))

    def test_retrieve_by_uuid(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.assertIs(ob, ob.__class__.by_uuid(ob.uuid))

    def test_retrieve_by_bad_uid(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.assertIs(None, ob.__class__.by_uuid('asdad'))

    def test_recipient_bounces_query(self):
        ob = self._makeOne()
        self.session.add(ob)
        self.session.flush()
        self.assertEqual(0, ob.recipient.bounces_query.count())
        ob.bounce_time = datetime.datetime.now()
        self.session.flush()
        self.assertEqual(1, ob.recipient.bounces_query.count())
