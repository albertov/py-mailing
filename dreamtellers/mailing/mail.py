import os
import logging
import smtplib
from itertools import chain
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email import Charset, Encoders
from email.Header import Header
Charset.add_charset('utf-8', Charset.SHORTEST, Charset.QP, 'utf-8')
Charset.add_charset('iso-8859-1', Charset.SHORTEST, Charset.QP, 'iso-8859-1')

import sx.pisa3 as pisa
from cStringIO import StringIO

from pkg_resources import resource_string, resource_filename
from lxml import etree
from lxml.cssselect import CSSSelector
import cssutils
from resumencm.lib.base import config, render, render_mako
from resumencm.lib.helpers import format_date

class RenderPDFError(StandardError): pass

log = logging.getLogger(__name__)

def _load_data(p):
    return resource_string('resumencm', os.path.join('public', p.lstrip('/')))

def embed_images(doc):
    doc = parse(doc)
    images = []
    for i, img_tag in enumerate(doc.xpath('//img')):
        img = MIMEImage(_load_data(img_tag.attrib['src']))
        img.add_header('Content-ID', '<image-%d>'%i)
        images.append(img)
        img_tag.attrib['src'] = 'cid:image-%d' % i
    return doc, images

def embed_styles(doc):
    doc = parse(doc)
    for link_tag in  doc.xpath('//link[@rel="stylesheet"]'):
        sheet = cssutils.parseString(_load_data(link_tag.attrib['href']))
        link_tag.getparent().remove(link_tag)
        for selector in sheet:
            for node in CSSSelector(selector.selectorText)(doc):
                styles = set(chain(*(s.split(';') for s in selector.style.cssText.split('\n'))))
                if 'style' in node.attrib:
                    old_styles = set(node.attrib['style'].split(';'))
                    old_styles.update(styles)
                    styles = old_styles
                node.attrib['style'] = '; '.join(filter(None, map(lambda s: s.strip(), styles)))
    return doc

static_path = resource_filename('resumencm', 'public')

def _link_cb(src, relative):
    path = os.path.abspath(os.path.join(static_path, src.lstrip('/')))
    return path


def render_pdf(mailing, subscriber):
    html = render('mailing/show.html', mailing=mailing, subscriber=subscriber)
    html = etree.tounicode(embed_styles(html), method='html')
    output = StringIO()
    enc = 'utf-8'
    pdf = pisa.CreatePDF(StringIO(html.encode(enc)), output, encoding=enc,
                         link_callback=_link_cb)
    if pdf.err:
        raise RenderPDFError
    return output.getvalue()

def parse(doc):
    if isinstance(doc, str):
        doc = etree.HTML(doc.decode('utf-8'))
    elif isinstance(doc, unicode):
        doc = etree.HTML(doc)
    return doc
    

    
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

def send_mailing(mailing, subscribers):
    smtp = open_smtp_connection()
    for subscriber in subscribers:
        log.info("Enviando %r a %r", mailing, subscriber)
        send_mailing_to_subscriber(mailing, subscriber, smtp=smtp)
        log.info("Enviado %r a %r con exito", mailing, subscriber)
    smtp.quit()

def send_mailing_to_subscriber(mailing, subscriber, send_pdf=False, smtp=None):
    token = mailing.generate_token(subscriber).token
    html = render('mailing/show.html', mailing=mailing, subscriber=subscriber,
                  token=token)
    text = render_mako('mailing/show.mako', mailing=mailing,
                       subscriber=subscriber, token=token)
    doc = parse(html)
    # remove content-type headers
    for meta in doc.xpath('//meta[@http-equiv]'):
        meta.getparent().remove(meta)
    doc, images = embed_images(doc)
    doc = embed_styles(doc)
    strFrom = config['resumencm.email_from']
    strTo = subscriber.email

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    subject = "Resumen de confidenciales de CapitalMadrid (%s)" % format_date(mailing.send_on, format='long', locale='es')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to
    # display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = SafeMIMEText(text, 'plain', 'utf-8')
    msgAlternative.attach(msgText)

    html =  etree.tounicode(doc, method='html')
    #open('test.html', 'w').write(html.encode('utf-8'))
    msgText = SafeMIMEText(html.encode('utf-8'), 'html', 'utf-8')
    msgAlternative.attach(msgText)

    map(msgRoot.attach, images)

    if send_pdf:
        # attach pdf
        fname = "resumen-confidenciales-CapitalMadrid-%s.pdf"
        fname = fname  % mailing.send_on.strftime("%Y%m%d")
        pdf = MIMEBase('application', 'pdf', name=fname)
        pdf.set_payload(render_pdf(mailing, subscriber))
        Encoders.encode_base64(pdf)
        pdf.add_header('Contet-Disposition', 'attachment; filename="%s"'%fname)
        msgRoot.attach(pdf)

    # Send the email (this example assumes SMTP authentication is required)
    if smtp is None:
        smtp = open_smtp_connection()
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    #smtp.quit()

def open_smtp_connection():
    smtp = smtplib.SMTP()
    smtp.connect(config['resumencm.email_server'])
    smtp.login(config['resumencm.email_user'], config['resumencm.email_passwd'])
    return smtp
