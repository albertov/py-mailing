#!/usr/bin/env python
#coding=utf8
from contextlib import contextmanager
import os, os.path
import subprocess
import tempfile
import urllib
import time
import json

from lxml import etree
from pkg_resources import resource_filename

DIR = resource_filename('mailing', 'static')
SENCHA = '/Applications/SenchaSDKTools-2.0.0-beta3/sencha'
LICENSE_TEXT = u'Copyright(c) 2012 Alberto Valverde González'

def main():
    jsb = os.path.join(DIR, 'app.jsb3')
    with running_server() as url:
        print "Creating JSB..."
        subprocess.check_call([SENCHA, 'create', 'jsb',
                               '-a', url,
                               '-p', 'app.jsb3'], cwd=DIR)

        print "Mangling jsb3..."
        mangle_jsb(url, jsb)
    print "Building minimized app..."
    subprocess.check_call([SENCHA, 'build',
                           '-p', 'app.jsb3', '-d', DIR], cwd=DIR)
    #os.unlink(jsb)
    
    
def mangle_jsb(url, fname, projectName='pyMailing', licenseText=LICENSE_TEXT):
    with open(fname, 'r') as f:
        data = json.load(f)
    data['projectName'] = projectName
    data['licenseText'] = licenseText
    for build in data['builds']:
        files = build['files']
        if build['target'] == 'app-all.js':
            dom = etree.parse(url)
            extra_files = []
            for script in dom.xpath('//script[@class="in-build"]'):
                src = script.attrib['src']
                parts = src.split('/')
                extra_files.append(dict(
                    path = '/'.join(parts[2:-1])+'/',
                    name = parts[-1]
                ))
            files[:0] = extra_files
        for file in files:
            path = file['path']
            path = path.replace('../static/', '').replace('/static', '')
            file['path'] = path
    with open(fname, 'w') as f:
        json.dump(data, f, encoding='utf8', indent=4)


@contextmanager
def running_server(port=60606, timeout=10):
    tmp_db = tempfile.TemporaryFile()
    bind = 'localhost:{0}'.format(port)
    print "Launching server at {0}...".format(bind)
    p = subprocess.Popen(['mailing',
                          '--db', tmp_db.name,
                          '--bind', bind,
                          '--debug'])
    url = 'http://{0}/admin/'.format(bind)
    print "Waiting for server to start up..."
    for _ in xrange(timeout):
        try:
            urllib.urlopen(url)
        except IOError:
            time.sleep(1)
        else:
            break
    print "Server ready"
    try:
        yield url
    finally:
        print "Terminating server"
        p.terminate()
        os.waitpid(p.pid, 0)

if __name__ == '__main__':
    main()
