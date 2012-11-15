import textwrap

from sqlalchemy import ForeignKey, Column, Integer, Unicode

from lxml import etree, builder

import markdown

from .item import Item

class ExternalLink(Item):
    __tablename__ = "external_link"
    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    content = Column(Unicode)
    url = Column(Unicode, nullable=False)
    __mapper_args__ = {'polymorphic_identity':'ExternalLink'}

    def __json__(self):
        return dict(super(ExternalLink, self).__json__(),
            content = self.content or None,
            url = self.url,
            )

class Article(Item):
    __tablename__ = 'article'
    __mapper_args__ = {'polymorphic_identity':'Article'}

    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    content = Column(Unicode, nullable=False)

    @property
    def url(self):
        return "#art-%d"%self.position

    @property
    def anchor(self):
        return "art-%d"%self.position


    @property
    def html(self):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.content))
        self._insert_image(dom)
        return '\n'.join(etree.tounicode(e, method='xml')
                         for e in dom.getchildren())

    def plain_text(self, width=79):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.content))
        for e in dom.xpath('//a'):
            if 'href' in e.attrib:
                e.tag = 'span'
                e.text += u' ({0})'.format(e.attrib.pop('href'))
        text = '\n\n'.join(etree.tounicode(e, method='text')
                         for e in dom.getchildren())
        return textwrap.fill(text, width)

    def _insert_image(self, dom):
        if self.image:
            ps = dom.xpath('//p[1]')
            if ps:
                p = ps[0]
                img = builder.E.img(src=self.image.filename)
                if self.image.title:
                    img.attrib['title'] = img.attrib['alt'] = self.image.title
                class_ = 'left' if self.image_position=='l' else 'right'
                img.attrib["class"] = class_
                p.insert(0, img)
                img.tail = p.text
                p.text = None

    def __json__(self):
        return dict(super(Article, self).__json__(),
            content = self.content,
            )


