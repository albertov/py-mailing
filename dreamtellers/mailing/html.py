from lxml import etree

from .util import collapse_styles
from .models import MissingTemplate

class HTMLPageComposer(object):

    doctypes = dict(
        strict =  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
        transitional = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
        html5 = '<!DOCTYPE html',
        )
    # Ver: http://www.emailonacid.com/blog/details/C13/ensure_that_your_entire_email_is_rendered_by_default_in_the_iphone_ipad
    min_head_length = 1019

    def __init__(self, mailing, encoding='utf-8', doctype='strict'):
        self._mailing = mailing
        self._encoding = encoding
        self._doctype = doctype

    @property
    def doctype(self):
        return self.doctypes[self._doctype]
        

    @property
    def files(self):
        yield 'index.html', self._generate_html()
        text = self._generate_text()
        if text:
            yield 'index.txt', text
        for img in self._mailing.images:
            yield img.filename, img.data

    def get_file(self, filename):
        if filename == 'index.html':
            return _HTMLFile(self._generate_html())
        elif filename == 'index.txt':
            text = self._generate_text()
            if text:
                return _TextFile(text)
        else:
            return self._mailing.get_file(filename)

        
    
    def _generate_html(self):
        dom = etree.HTML(self._mailing.render('xhtml'))
        self._collapse_styles(dom)
        self._insert_head_padding(dom)
        #TODO: Extract encoding from <meta http-equiv=""> if present
        encoding = self._encoding
        return self._serialize(dom, True).encode(encoding)

    def _generate_text(self):
        try:
            return self._mailing.render('text').encode(self._encoding)
        except MissingTemplate:
            return None

    def _insert_head_padding(self, dom):
        try:
            head = dom.xpath('//head')[0]
        except IndexError:
            return
        head_html = '\n'.join(self._serialize(e) for e in head.getchildren())
        pad_amount = self.min_head_length - len(head_html)
        if pad_amount>0:
            head.getchildren()[-1].tail = ' '*pad_amount


    def _collapse_styles(self, dom):
        collapse_styles(dom)

    def _serialize(self, dom, with_doctype=False):
        return etree.tounicode(dom, method='xml',
                               doctype=self.doctype if with_doctype else None)

class _HTMLFile(object):
    content_type = 'text/html; charset=utf-8'
    def __init__(self, data):
        self.data = data

class _TextFile(object):
    content_type = 'text/plain; charset=utf-8'
    def __init__(self, data):
        self.data = data
