from cStringIO import StringIO

from lxml import etree
from ftputil import FTPHost

from .util import collapse_styles

class HTMLPageComposer(object):
    FTPHost = FTPHost  # for mock inyection in tests

    def __init__(self, mailing, encoding='utf-8'):
        self._mailing = mailing
        self._encoding = encoding

    def upload_to_ftpsite(self, host, username, password, dir='/'):
        with self.FTPHost(host, username, password) as ftp:
            ftp.makedirs(dir)
            dir = dir.rstrip('/') + '/'
            for fname, data in self.files:
                dest = ftp.file(dir+fname, 'w')
                ftp.copyfileobj(StringIO(data), dest)
                dest.close()
        

    @property
    def files(self):
        html = self._generate_html()
        yield 'index.html', html.encode(self._encoding)
        for img in self._mailing.images:
            yield img.filename, img.data
    
    def _generate_html(self):
        dom = etree.HTML(self._mailing.render('xhtml'))
        self._collapse_styles(dom)
        return etree.tounicode(dom, method='html')

    def _collapse_styles(self, dom):
        collapse_styles(dom)

