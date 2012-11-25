#coding=utf8
from __future__ import with_statement
try:
    import json
except ImportError:
    import simplejson as json
from glob import glob
import os
import datetime

from pkg_resources import resource_filename

from lxml import etree

from ..models import BaseModelTest

                      
        

def fixture(s):
    return resource_filename(__name__, s)


class TestCalistoMailing(BaseModelTest):

    def _makeMailing(self, **kw):
        return mailing_from_fixture(fixture('data.json'), **kw)
    
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
        self.failUnlessEqual(len(m.items), 14)
        self.failUnlessEqual(len(m.items_by_type('Article')), 14)
        self.failUnlessEqual(len(m.items_by_type('ExternalLink')), 0)

    def test_correct_images(self):
        m = self._makeMailing()
        self.failUnlessEqual(len(m.images), 19)

    def test_can_render(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        self.failUnless(isinstance(html, unicode), type(html))

    def test_renders_valid_xhtml(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        etree.fromstring(html)

    def test_contains_expected_elements(self):
        m = self._makeMailing()
        html = m.render('xhtml')
        dom = etree.HTML(html)
        self.failUnlessEqual(len(dom.xpath("//*[@class='seccion']")), 4)

    def test_number_is_formatted(self):
        self.assertIn(u'nº 004',
            self._makeMailing(number=4).render('xhtml'))
        

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

def mailing_from_fixture(fname, number=0, date=datetime.datetime.now()):
    from ...models import (Mailing, Image, Article, ExternalLink, Template,
                           Category, Session)
    
    data = json.load(open(fname))
    mailing = Mailing(number=number, date=date)

    for f in glob(fixture('template/*')):
        if f.split('.')[-1] in ('gif', 'png', 'jpg', 'jpeg'):
            with open(f) as file:
                f = os.path.basename(f)
                img = Image(filename=f, data=file.read())
                Session.add(img)
    Session.flush()

    body = open(fixture('template/index.html')).read().decode('utf8')
    mailing.templates['xhtml'] = Template(title="Calisto 1", body=body)

    body = open(fixture('template/index.txt')).read().decode('utf8')
    mailing.templates['text'] = Template(title="Calisto 1 (texto)", body=body,
                                         type='text')


    for cat_data in data['categories']:
        cat = Category(title=cat_data['title'])
        if 'logo' in cat_data:
            cat.image = Image.by_filename(cat_data['logo'])
            cat.image.title = cat.title
        for item_data in cat_data['items']:
            if 'link' in item_data:
                item = ExternalLink(url=item_data['link'],
                                    title=item_data['title'])
            else:
                item = Article(content=item_data['text'],
                               title=item_data['title'])
                image = item_data.get('image')
                if image:
                    path = os.path.join(os.path.dirname(os.path.abspath(fname)),
                                        image['path'])
                    assert os.path.exists(path), path
                    item.image = Image(data=open(path).read(),
                                       filename=image['path'],
                                       title=image['title'])
            item.category = cat
            mailing.items.append(item)

    return mailing
