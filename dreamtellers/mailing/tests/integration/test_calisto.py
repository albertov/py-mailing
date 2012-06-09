import os
import datetime
import json
from unittest import TestCase
from glob import glob

from pkg_resources import resource_filename

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

    def test_create_and_persist(self):
        m = self._makeMailing()
        self.session.add(m)
        self.session.commit()
