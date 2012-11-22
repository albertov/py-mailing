import json
import HTMLParser

from ...models import Image
from ...models.image import _pil_image
from . import BaseViewTest


class TestImageView(BaseViewTest):
    def test_create_a_good_one(self):
        data = Image.blank_image(1, 1,'image/png')
        data = dict(title='foo', filename='foo.gif', data=data.encode('hex'))
        resp = self.app.post_json('/image/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['images']), 1)
        item = resp.json['images'][0]
        expected = {
            u'content_type': u'image/png',
            u'filename': u'foo.gif',
            u'title': u'foo'
            }
        for k in expected:
            self.assertEqual(expected[k], item[k])

    def test_create_non_image(self):
        data = dict(title='foo', filename='foo.gif',
                    data='Not an image'.encode('hex'))
        resp = self.app.post_json('/image/', data, status=400)
        self.assertFalse(resp.json['success'])

    def test_create_bad_encoding(self):
        data = dict(title='foo', filename='foo.gif',
                    data='Not an image')
        resp = self.app.post_json('/image/', data, status=400)
        self.assertFalse(resp.json['success'])
        

    def test_upload_one(self):
        data = Image.blank_image(1, 1,'image/png')
        resp = self.app.post('/image/upload', {'title':'foo'},
                             upload_files=[('image', 'foo.gif', data)])
        self.assertEqual(resp.content_type, 'text/html')
        h = HTMLParser.HTMLParser()
        resp_data = json.loads(h.unescape(resp.body))
        self.assertTrue(resp_data['success'])
        self.assertEqual(len(resp_data['images']), 1)
        item = resp_data['images'][0]
        expected = {
            u'content_type': u'image/png',
            u'filename': u'foo.gif',
            u'title': u'foo'
            }
        for k in expected:
            self.assertEqual(expected[k], item[k])

    def test_upload_non_image(self):
        data = 'Im not an image!'
        resp = self.app.post('/image/upload', {'title':'foo'},
                             upload_files=[('image', 'foo.gif', data)],
                             status=400)
        self.assertEqual(resp.content_type, 'text/html')
        h = HTMLParser.HTMLParser()
        resp_data = json.loads(h.unescape(resp.body))
        self.assertFalse(resp_data['success'])

    def test_view_non_exting_image(self):
        resp = self.app.get('/image/4523453245234/view', status=404)

    def test_view_image(self):
        content_type = 'image/png'
        data = Image.blank_image(1, 1, content_type)
        resp = self.app.post('/image/upload', {'title':'foo'},
                             upload_files=[('image', 'foo.gif', data)])
        self.assertEqual(resp.content_type, 'text/html')
        h = HTMLParser.HTMLParser()
        resp_data = json.loads(h.unescape(resp.body))
        self.assertTrue(resp_data['success'])
        self.assertEqual(len(resp_data['images']), 1)
        item = resp_data['images'][0]
        resp = self.app.get(item['internal_url'])
        self.assertEqual(resp.content_type, content_type)
        self.assertEqual(resp.body, data)

    def test_view_image_thumbnail(self):
        content_type = 'image/png'
        data = Image.blank_image(100, 100, content_type)
        resp = self.app.post('/image/upload', {'title':'foo'},
                             upload_files=[('image', 'foo.gif', data)])
        self.assertEqual(resp.content_type, 'text/html')
        h = HTMLParser.HTMLParser()
        resp_data = json.loads(h.unescape(resp.body))
        self.assertTrue(resp_data['success'])
        self.assertEqual(len(resp_data['images']), 1)
        item = resp_data['images'][0]
        resp = self.app.get(item['internal_url']+'?width=10&height=10')
        self.assertEqual(resp.content_type, content_type)
        im = _pil_image(resp.body)
        self.assertEqual(im.size, (10,10))
