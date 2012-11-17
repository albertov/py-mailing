import datetime

from unittest2 import TestCase


class BaseModelTest(TestCase):

    def setUp(self):
        from ...models import Session, Model, create_engine
        self.engine = create_engine('sqlite://')
        Model.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session

    def tearDown(self):
        self.session.remove()

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
        return Template(**kw)

    def _makeCategory(self, **kw):
        from ...models import Category
        kw.setdefault('title', 'CategoryTitle')
        return Category(**kw)

    def _makeGroup(self, **kw):
        from ...models import Group
        return Group(**kw)

    def _makeRecipient(self, **kw):
        from ...models import Recipient
        return Recipient(**kw)

    def _makeSentMailing(self, **kw):
        from ...models import SentMailing
        return SentMailing(**kw)
