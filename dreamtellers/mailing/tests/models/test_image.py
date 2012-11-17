from . import BaseModelTest
from ...models.image import _pil_image


class TestConfig(BaseModelTest):

    def _makeOne(self):
       return self._makeImage() 

    def test_blank_image(self):
        ob = self._makeOne()
        ctype = 'image/png'
        ob.data = ob.blank_image(100, 100, ctype)
        self.failUnless(ob.content_type, ctype)

    def test_blank_image(self):
        ob = self._makeOne()
        ctype = 'image/png'
        width, height = 100, 50
        im = _pil_image(ob.blank_image(width, height, ctype))
        try:
            im.verify()
        except Exception, e:
            self.fail(e)
        self.assertEqual(im.size, (width, height))

    def test_thumbnail(self):
        ob = self._makeOne()
        ctype = 'image/png'
        width, height = 100, 50
        ob.data = ob.blank_image(width, height, ctype)
        twidth, theight = 10, 5
        thumbnail = ob.thumbnail(twidth, theight)
        im = _pil_image(thumbnail)
        try:
            im.verify()
        except Exception, e:
            self.fail(e)
        self.assertEqual(im.size, (twidth, theight))
