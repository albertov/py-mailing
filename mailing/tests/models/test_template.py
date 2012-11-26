import random
import datetime

from . import BaseModelTest


class TestTemplate(BaseModelTest):
    _makeOne = BaseModelTest._makeTemplate

    def test_create(self):
        self.failUnless(self._makeOne())

    def test_repr(self):
        ob = self._makeOne()
        self.assertIn('Template', repr(ob))

    def test_content_type(self):
        ob = self._makeOne(type='xhtml')
        self.assertEqual('text/html', ob.content_type)
        ob = self._makeOne(type='text')
        self.assertEqual('text/plain', ob.content_type)



    def test_render_good_xhtml(self):
        ob = self._makeOne(
            type='xhtml',
            body=('<html xmlns:py="http://genshi.edgewall.org/">'
                  '<body><div py:content="foo" /></body></html>')
            )
        output = ob.render(foo='bar')
        expected = '<html><body><div>bar</div></body></html>'
        self.assertEqual(expected, output)

    def test_render_xhtml_template_with_syntax_error(self):
        ob = self._makeOne(
            type='xhtml',
            debug=True,
            body=('<html xmlns:py="http://genshi.edgewall.org/">\n'
                  '<body><div py:content="foo + 2" /></body></html>')
            )
        output = ob.render(foo='bar')
        self.assertIn(
            'cannot concatenate &#39;str&#39; and &#39;int&#39; objects',
            output)
        self.assertIn('<span>2:</span><span style="color:#f00">', output)

    def test_render_xhtml_template_with_template_syntax_error(self):
        ob = self._makeOne(
            type='xhtml',
            debug=True,
            body=('<html xmlns:py="http://genshi.edgewall.org/">\n'
                  '<body><div py:contents="foo" /></body></html>')
            )
        output = ob.render(foo='bar')
        self.assertIn('bad directive "contents"', output)
        self.assertIn('<span>2:</span><span style="color:#f00">', output)

    def test_render_xhtml_template_with_undefined_variable_error(self):
        ob = self._makeOne(
            type='xhtml',
            debug=True,
            body=('<html xmlns:py="http://genshi.edgewall.org/">\n'
                  '<body><div py:content="foos" /></body></html>')
            )
        output = ob.render(foo='bar')
        self.assertIn('"foos" not defined', output)
        self.assertIn('<span>2:</span><span style="color:#f00">', output)

    def test_render_good_text(self):
        ob = self._makeOne(
            type='text',
            body='Hello Mr. ${foo}'
            )
        output = ob.render(foo='bar')
        expected = 'Hello Mr. bar'
        self.assertEqual(expected, output)

    def test_render_text_with_syntax_error(self):
        ob = self._makeOne(
            type='text',
            body='Hello Mr. ${foo+2}',
            debug=True
            )
        output = ob.render(foo='bar')
        self.assertIn('cannot concatenate \'str\' and \'int\' objects', output)

    def test_render_text_with_undefined_variable_error(self):
        ob = self._makeOne(
            type='text',
            body='Hello Mr. ${foos}',
            debug=True
            )
        output = ob.render(foo='bar')
        self.assertIn('Undefined', output)
