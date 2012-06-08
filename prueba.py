import sys
import datetime
import json
from dreamtellers.mailing.models import *

session = create_sessionmaker()()

def importa_mailing(number, date, data):
    mailing = Mailing(number=number, date=date)
    mailing.template = FilesystemTemplate(title="Calisto 1",
                                          path="mailing.html",
                                          serializer='xhtml')
    for cat_data in data['categories']:
        cat = Category(title=cat_data['title'])
        if 'logo' in cat_data:
            logo = Image(path=cat_data['logo'], title=cat.title)
            cat.image = logo
        for item_data in cat_data['items']:
            if 'link' in item_data:
                item = ExternalLink(url=item_data['link'],
                                    title=item_data['title'])
            else:
                item = Article(text=item_data['text'],
                               title=item_data['title'])
            item.category = cat
            mailing.items.append(item)
    return mailing


if __name__ == '__main__':
    m = importa_mailing(1, datetime.datetime(2012,6,9), json.load(sys.stdin))
    with open(sys.argv[1], 'w') as f:
        f.write(m.render())
