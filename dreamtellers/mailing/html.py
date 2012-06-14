from lxml import etree

from .util import collapse_styles

class HTMLPageComposer(object):

    def __init__(self, mailing, encoding='utf-8'):
        self._mailing = mailing
        self._encoding = encoding
        

    @property
    def files(self):
        yield 'index.html', self._generate_html()
        for img in self._mailing.images:
            yield img.filename, img.data

    def get_file(self, filename):
        if filename == 'index.html':
            return _HTMLFile(self._generate_html())
        return self._mailing.get_file(filename)

        
    
    def _generate_html(self):
        dom = etree.HTML(self._mailing.render('xhtml'))
        self._collapse_styles(dom)
        #TODO: Extract encoding from <meta http-equiv=""> if present
        encoding = self._encoding
        return etree.tounicode(dom, method='html').encode(encoding)

    def _collapse_styles(self, dom):
        collapse_styles(dom)

class _HTMLFile(object):
    content_type = 'text/html; charset=utf-8'
    def __init__(self, data):
        self.data = data
