from itertools import chain
import logging

import cssutils
from lxml.cssselect import CSSSelector, ExpressionError

log = logging.getLogger(__name__)

def collapse_styles(dom):
    """
    Collects CSS declarations from <style> nodes and <link rel="stylesheet">
    elements and applies them to selected nodes as `style` attributes
    """
    for style in dom.xpath('//style'):
        sheet = cssutils.parseString(style.text)
        style.getparent().remove(style)
        for selector in sheet:
            try:
                xpath = CSSSelector(selector.selectorText)
            except ExpressionError, e:
                log.warn("Could not internalize selector %r because: %s",
                         selector.selectorText, e)
                continue
            for node in xpath(dom):
                styles = set(chain(*(
                    s.split(';') for s in selector.style.cssText.split('\n')
                )))
                if 'cstyle' in node.attrib:
                    old_styles = node.attrib['cstyle'].split(';')
                    old_styles.extend(styles)
                    styles = old_styles
                style = '; '.join(filter(None, [s.strip() for s in styles]))
                node.attrib['cstyle'] = style
    for e in dom.xpath('//*[@cstyle]'):
        if 'style' in e.attrib:
            styles = e.attrib['style'].split(';')
        else:
            styles = []
        computed_styles = e.attrib['cstyle'].split(';')
        del e.attrib['cstyle']
        e.attrib['style'] = ';'.join(computed_styles+styles)
