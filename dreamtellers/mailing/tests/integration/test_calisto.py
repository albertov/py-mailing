import os
import datetime
import json
from unittest import TestCase
from glob import glob

from pkg_resources import resource_filename

from lxml import etree

                      
        

def fixture(s):
    return resource_filename(__name__, s)


class TestCalistoMailing(TestCase):

    def setUp(self):
        self.session = self._makeSession()

    def _makeSession(self):
        from ...models import create_sessionmaker
        return create_sessionmaker()()

    def _loadData(self):
        return json.load(open(fixture('data.json')))

    def _makeMailing(self):
        return mailing_from_fixture(self._loadData())
    
    def _makeHTMLPageComposer(self, mailing=None):
        if mailing is None:
            mailing = self._makeMailing()
        from ...html import HTMLPageComposer
        return HTMLPageComposer(mailing)

    def _makeMessageComposer(self, mailing=None):
        if mailing is None:
            mailing = self._makeMailing()
        from ...mail import MessageComposer
        return MessageComposer(mailing)

    def test_create_persist_retrieve(self):
        ob = self._makeMailing()
        self.session.add(ob)
        self.session.commit()
        self.session.expunge_all()

        m = self.session.query(ob.__class__).one()
        self.failUnless(m)

    def test_correct_items(self):
        m = self._makeMailing()
        self.failUnlessEqual(len(m.items), 13)
        self.failUnlessEqual(len(m.items_by_type('Article')), 9)
        self.failUnlessEqual(len(m.items_by_type('ExternalLink')), 4)

    def test_correct_images(self):
        m = self._makeMailing()
        self.failUnlessEqual(len(m.images), 11)
        self.failUnlessEqual(len([i for i in m.images if i.content_type=='image/gif']), 9)
        self.failUnlessEqual(len([i for i in m.images if i.content_type=='image/png']), 2)
        self.failUnlessEqual(len([i for i in m.images if i.title]), 4)

    def test_can_render(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        self.failUnless(isinstance(html, unicode), type(html))

    def test_renders_valid_xhtml(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        dom = etree.fromstring(html)

    def test_contains_expected_elements(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        dom = etree.HTML(html)
        self.failUnlessEqual(len(dom.xpath("//*[@class='seccion']")), 4)

    def test_email_message(self):
        m = self._makeMailing()
        composer = self._makeMessageComposer(m)
        msg = composer.generate_message()
        body = str(msg)
        self.failUnless('image/png' in body)
        self.failUnless('image/gif' in body)
        self.failUnless('text/html' in body)

    def test_html_compposer(self):
        m = self._makeMailing()
        composer = self._makeHTMLPageComposer(m)
        files = dict(composer.files)
        self.failUnless('index.html' in files)
        for img in m.images:
            self.failUnless(img.filename in files)
        for fname, data in files.items():
            self.failUnlessEqual(composer.get_file(fname).data, data)

def mailing_from_fixture(data, number=1, date=datetime.datetime.now()):
    from ...models import (Mailing, Image, Article, ExternalLink, Template,
                           Category)

    mailing = Mailing(number=number, date=date)

    body = open(fixture('template/index.html')).read().decode('utf8')
    mailing.templates['xhtml'] = Template(title="Calisto 1", body=body)

    images = {}
    for f in glob(fixture('template/*')):
        if f.split('.')[-1] in ('gif', 'png'):
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