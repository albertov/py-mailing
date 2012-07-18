import re
import logging
from base64 import b64encode

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email import Encoders
from email.Header import Header

import cssutils

from lxml import etree

from .util import collapse_styles
from .models import MissingTemplate

def _add_email_charsets():
    from email import Charset
    Charset.add_charset('utf-8', Charset.SHORTEST, Charset.QP, 'utf-8')
    Charset.add_charset('iso-8859-1', Charset.SHORTEST, Charset.QP,
                        'iso-8859-1')

_add_email_charsets()

log = logging.getLogger(__name__)

class MultipartMessage(object):
    def __init__(self, encoding='utf-8'):
        self._encoding = encoding
        self._msg = MIMEMultipart('related')
        self._alternative = MIMEMultipart('alternative')
        self._msg.attach(self._alternative)
        self._msg.preamble = 'This is a multi-part message in MIME format.'

    def add_text(self, content, type='plain'):
        part = SafeMIMEText(self._encode(content), type, self._encoding)
        self._alternative.attach(part)

    def add_image(self, data, id, content_type=None):
        subtype = content_type.split('/')[-1] if content_type else None
        img = MIMEImage(data, subtype)
        img.add_header('Content-ID', '<{0}>'.format(id))
        img.add_header('Content-Disposition', 'inline')
        self._msg.attach(img)

    def add_attachment(self, filename, payload, content_type='octet/stream'):
        filename = self._encode(filename)
        attachment = MIMEBase(*content_type.split('/'), name=filename)
        attachment.set_payload(payload)
        Encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'Attachment; filename="%s"'%filename)
        self._msg.attach(attachment)

    def add_header(self, name, value):
        self._msg[name] = self._encode(value)

    def get_header(self, name):
        return self._msg[name]
        
    def del_header(self, name):
        del self._msg[name]
        
    def _encode(self, text):
        if isinstance(text, unicode):
            text = text.encode(self._encoding)
        return text

    def __str__(self):
        return self._msg.as_string()
        
class MessageComposer(object):
    _url_re = re.compile(r'url\(["\']{0,1}(.*?)["\']{0,1}\)')
    missing_template_text = "This is a HTML only message"

    def __init__(self, mailing, encoding='utf-8'):
        self._mailing = mailing
        self._encoding = encoding

    def generate_message(self):
        html, encoding = self._generate_html()
        msg = MultipartMessage(encoding)
        text = self._generate_text()
        msg.add_text(text, 'plain')
        msg.add_text(html, 'html')
        for img in self._mailing.images:
            #TODO: NO incluir las imagenes ya incluidas como data:
            msg.add_image(img.data,
                          self._content_id(img.filename),
                          img.content_type)
        return msg

    def _generate_text(self):
        try:
            return self._mailing.render('text')
        except MissingTemplate:
            return self.missing_template_text

    def _generate_html(self):
        dom = etree.HTML(self._mailing.render('xhtml'))
        self._remove_http_equiv_headers(dom)
        self._collapse_styles(dom)
        self._internalize_images(dom)
        #TODO: Extract encoding from <meta http-equiv=""> if present
        encoding = self._encoding
        return etree.tounicode(dom, method='html'), encoding


    def _remove_http_equiv_headers(self, dom):
        for meta in dom.xpath('//meta[@http-equiv]'):
            meta.getparent().remove(meta)

    def _internalize_images(self, dom):
        for img in dom.xpath('//img'):
            img.attrib['src'] = 'cid:' + self._content_id(img.attrib['src'])

        for e in dom.xpath('//*[@background]'):
            e.attrib['background'] = 'cid:' + self._content_id(e.attrib['background'])
        for e in dom.xpath('//*[@style]'):
            e.attrib['style'] = self._embed_image_data(e.attrib['style'])
        for e in dom.xpath('//style'):
            e.text = self._embed_image_data.sub(e.text)

    def _content_id(self, src):
        return src + '@dreamtellers.mailing'

    def _embed_image_data(self, txt):
        def repl(m):
            src = m.group(1)
            try:
                img = [i for i in self._mailing.images if i.filename==src][0]
            except IndexError:
                # Not an internal image, leave it as-is
                return m.group(0)
            data = b64encode(img.data)
            return "url(data:{0};base64,{1})".format(img.content_type, data)
        return self._url_re.sub(repl, txt)

    def _collapse_styles(self, dom):
        collapse_styles(dom)


class BadHeaderError(ValueError):
    pass

class SafeHeaderMixin(object):
    def __setitem__(self, name, val):
        "Forbids multi-line headers, to prevent header injection."
        if '\n' in val or '\r' in val:
            raise BadHeaderError, "Header values can't contain newlines (got %r for header %r)" % (val, name)
        if name == "Subject":
            val = Header(val, 'utf-8')
        # Note: using super() here is safe; any __setitem__ overrides must use
        # the same argument signature.
        super(SafeHeaderMixin, self).__setitem__(name, val)

class SafeMIMEText(MIMEText, SafeHeaderMixin):
    pass
