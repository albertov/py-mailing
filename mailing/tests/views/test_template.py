#coding=utf8
try:
    import json
except ImportError:
    import simplejson as json
import HTMLParser

from ...models import Image
from ...models.image import _pil_image
from . import BaseViewTest



class TestTemplate(BaseViewTest):
    def test_create_xhtml_no_body(self):
        data = dict(title='foo', type='xhtml', body=None)
        resp = self.app.post_json(self.get_url('templates'), data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['templates']), 1)
        item = resp.json['templates'][0]
        expected = {
            u'title': u'foo',
            u'type': u'xhtml',
            }
        for k in expected:
            self.assertEqual(expected[k], item[k])
        from ...views.template import TemplateValidator
        self.maxDiff = None
        body = item['body']
        expected = TemplateValidator.default_bodies['xhtml']
        self.assertEqual(expected, body)

    def test_create_xhtml_bad_body(self):
        data = dict(title='foo', type='xhtml', body='<html></div>')
        resp = self.app.post_json(self.get_url('templates'), data, status=400)
        self.assertFalse(resp.json['success'])
        self.assertIn('body', resp.json['errors'])
        self.assertIn('Invalid XML: Opening and ending tag mismatch',
                      resp.json['errors']['body'])


    def test_upload_body(self):
        # Create initial
        data = dict(title='foo', type='xhtml', body=None)
        resp = self.app.post_json(self.get_url('templates'), data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['templates']), 1)

        # Post updated bopy
        id = resp.json['templates'][0]['id']
        new_body = '<html>Foo</html>\n'
        resp = self.app.post(self.get_url('template.upload', id=id),
                             {'type':'xhtml'},
                             upload_files=[('body', 'file.html', new_body)])
        self.assertEqual(resp.content_type, 'text/html')
        resp_data = self.json_from_html_body(resp.body)
        self.assertTrue(resp_data['success'])
        self.assertEqual(len(resp_data['templates']), 1)
        item = resp_data['templates'][0]
        self.assertEqual(data['title'], item['title'])
        self.assertEqual(new_body, item['body'])

    def test_upload_bad_body(self):
        # Create initial
        data = dict(title='foo', type='xhtml', body=None)
        resp = self.app.post_json(self.get_url('templates'), data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['templates']), 1)

        # Post updated bopy
        id = resp.json['templates'][0]['id']
        new_body = '<html>Foo</div>'
        resp = self.app.post(self.get_url('template.upload', id=id),
                             {'type':'xhtml'},
                             upload_files=[('body', 'file.html', new_body)],
                             status=400)
        self.assertEqual(resp.content_type, 'text/html')
        resp_data = self.json_from_html_body(resp.body)
        self.assertFalse(resp_data['success'])
        self.assertIn('body', resp_data['errors'])
        self.assertIn('Invalid XML: Opening and ending tag mismatch',
                      resp_data['errors']['body'])

    def test_raw_html_body(self):
        # Create initial
        data = dict(title=u'Avión', type='xhtml', body='<html/>\n')
        resp = self.app.post_json(self.get_url('templates'), data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['templates']), 1)
        id = resp.json['templates'][0]['id']

        resp = self.app.get(self.get_url('template.body', id=id))
        self.assertEqual('text/html', resp.content_type)
        self.assertEqual(data['body'], resp.body)
        self.assertIn('content-disposition', resp.headers)
        self.assertIn(data['title'],
                      resp.headers['content-disposition'].decode('utf8'))

    def test_raw_text_body(self):
        # Create initial
        data = dict(title=u'Avión', type='text', body='lala')
        resp = self.app.post_json(self.get_url('templates'), data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['templates']), 1)
        id = resp.json['templates'][0]['id']

        resp = self.app.get(self.get_url('template.body', id=id))
        self.assertEqual('text/plain', resp.content_type)
        self.assertEqual(data['body'], resp.body)
        self.assertIn('content-disposition', resp.headers)
        self.assertIn(data['title'],
                      resp.headers['content-disposition'].decode('utf8'))
