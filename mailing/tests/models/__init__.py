import os
import datetime

from unittest2 import TestCase

ENVIRON_DB_URL_KEY = 'PYMAILING_TEST_DB_URL'


class BaseModelTest(TestCase):
    engine = None

    def setUp(self):
        super(BaseModelTest, self).setUp()
        from ...models import Session, Model, create_engine
        url = os.environ.get(ENVIRON_DB_URL_KEY, 'sqlite://')
        if self.engine is None:
            # Cache engine as a classattr in BaseModel
            BaseModelTest.engine = create_engine(url)
        Model.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session

    def tearDown(self):
        self.session.remove()
        super(BaseModelTest, self).tearDown()

    def _makeMailing(self, **kw):
        from ...models import Mailing
        kw.setdefault('date', datetime.datetime(2010,1,1))
        return Mailing(**kw)

    def _makeExternalLink(self, **kw):
        from ...models import ExternalLink
        return ExternalLink(**kw)

    def _makeArticle(self, **kw):
        from ...models import Article
        return Article(**kw)

    def _makeImage(self, **kw):
        from ...models import Image
        return Image(**kw)

    def _makeTemplate(self, **kw):
        from ...models import Template
        defaults = dict(title='fooo', body='foo')
        return Template(**dict(defaults, **kw))

    def _makeCategory(self, **kw):
        from ...models import Category
        kw.setdefault('title', 'CategoryTitle')
        return Category(**kw)

    def _makeGroup(self, **kw):
        from ...models import Group
        return Group(**kw)

    def _makeRecipient(self, **kw):
        from ...models import Recipient
        defaults = dict(name='foo', email='email@example.com')
        return Recipient(**dict(defaults, **kw))

    def _makeMailingDelivery(self, **kw):
        from ...models import MailingDelivery
        return MailingDelivery(**kw)

    def _makeMailingDeliveryProcessedRecipient(self, *args, **kw):
        from ...models.mailing import MailingDeliveryProcessedRecipient
        return MailingDeliveryProcessedRecipient(*args, **kw)
