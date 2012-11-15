import logging
import os.path
import glob
import re
from itertools import chain
from cStringIO import StringIO

from pkg_resources import resource_filename
import cssutils
from lxml.cssselect import CSSSelector, ExpressionError

from .magic import from_buffer as magic_from_buffer

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
            if not hasattr(selector, 'selectorText'):
                # salta comentarios
                continue
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
                keys = []
                values = {}
                for s in styles:
                    if s.strip():
                        key, value = [v.strip() for v in s.split(':')]
                        if key not in keys:
                            keys.append(key)
                        values[key] = value
                style = '; '.join(':'.join([k, values[k]]) for k in keys)
                node.attrib['cstyle'] = style
    for e in dom.xpath('//*[@cstyle]'):
        if 'style' in e.attrib:
            styles = e.attrib['style'].split(';')
        else:
            styles = []
        computed_styles = e.attrib['cstyle'].split(';')
        del e.attrib['cstyle']
        e.attrib['style'] = ';'.join(computed_styles+styles)

def sniff_content_type(data):
    return magic_from_buffer(StringIO(data), 'mime')

def import_all_modules_from_package(package_name, exclude=('__init__',)):
    """Imports all modules in current package"""
    modules = [os.path.basename(f)[:-3]
             for f in glob.glob(resource_filename(package_name, '*.py'))
             if os.path.basename(f) not in exclude]
    __import__(package_name, fromlist=modules, level=1) 


def iter_config_key_values(top='.', exclude=('tests',)):
    regexp = re.compile(
        r'Config.setdefault\(\s*["\'](.*?)[\'"]\s*,\s*(.*?)\s*\)',
        re.MULTILINE) 
    ret = []
    def callback(func, dir, files):
        for f in files:
            if f in exclude:
                files.remove(f)
            elif f.endswith('.py'):
                func(os.path.join(dir, f))
    def scan(fname):
        with open(fname) as f:
            for m in regexp.finditer(f.read()):
                k, v = m.group(1), eval(m.group(2))
                ret.append((fname, k, v))
    os.path.walk(top, callback, scan)
    return ret

def prepopulate_config(top='.', exclude=('tests',)):
    from .models import Config
    for fname, key, value in iter_config_key_values(top, exclude):
        print repr((fname, key, value))
        Config[key] = value
