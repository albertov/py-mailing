import os
import datetime
import json
from unittest import TestCase
from glob import glob

from pkg_resources import resource_filename

from lxml import etree

from ...models import *

def fixture(s):
    return resource_filename(__name__, s)


class BaseModelTest(TestCase):

    def setUp(self):
        self.session = self._makeSession()

    def _makeSession(self):
        return create_sessionmaker()()

    def _loadData(self):
        return json.load(open(fixture('data.json')))

    def _makeMailing(self):
        number = 1
        date = datetime.datetime(2012,6,9)
        data = self._loadData()

        mailing = Mailing(number=number, date=date)

        body = open(fixture('template/index.html')).read().decode('utf8')
        mailing.templates['xhtml'] = Template(title="Calisto 1", body=body)

        images = {}
        for f in glob(fixture('template/*.gif')):
            fname = os.path.basename(f)
            with open(f) as file:
                images[fname] = Image(filename=fname, data=file.read())

        for cat_data in data['categories']:
            cat = Category(title=cat_data['title'])
            if 'logo' in cat_data:
                cat.image = images[cat_data['logo']]
                cat.image.title = cat.title
            for item_data in cat_data['items']:
                if 'link' in item_data:
                    item = ExternalLink(url=item_data['link'],
                                        title=item_data['title'])
                else:
                    item = Article(text=item_data['text'],
                                   title=item_data['title'])
                item.category = cat
                mailing.items.append(item)

        tpl = mailing.templates['xhtml']
        for i in images.values():
            if i.title is None:
                # no es imagen de categoria
               tpl.images.append(i)
        return mailing

    def test_create_persist_retrieve(self):
        self.session.add(self._makeMailing())
        self.session.commit()
        self.session.expunge_all()

        m = self.session.query(Mailing).one()
        self.failUnless(m)

    def test_correct_items(self):
        m = self._makeMailing()
        self.failUnlessEqual(len(m.items), 13)
        self.failUnlessEqual(len(m.items_by_type('Article')), 9)
        self.failUnlessEqual(len(m.items_by_type('ExternalLink')), 4)

    def test_correct_images(self):
        m = self._makeMailing()
        self.failUnlessEqual(len(m.images), 10)
        self.failUnlessEqual(len([i for i in m.images if i.title]), 4)

    def test_can_render(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        dom = etree.HTML(html)
        self.failUnlessEqual(len(dom.xpath("//div[@class='seccion']")), 4)
