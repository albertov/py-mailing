#coding: utf8
from .test_models import BaseModelTest
from ..models import Config


class TestConfig(BaseModelTest):
    def test_getsetitem(self):
        Config['foo'] = 4
        self.assertIsInstance(Config['foo'], int)
        self.assertEqual(Config['foo'], 4)

    def test_update_key(self):
        Config['foo'] = 4
        self.assertEqual(Config['foo'], 4)
        Config['foo'] = 'car'
        self.assertEqual(Config['foo'], 'car')

    def test_get_unknown_key(self):
        self.assertRaises(KeyError, Config.__getitem__, 'foo')

    def test_det_unknown_key(self):
        self.assertRaises(KeyError, Config.__delitem__, 'foo')

    def test_non_str_key(self):
        self.assertRaises(TypeError, Config.__setitem__, 2, 4)

    def test_iter(self):
        Config['foo'] = 4
        Config['bar'] = 6
        self.assertEqual(set(Config), set(['foo', 'bar']))

    def test_delitem(self):
        Config['foo'] = 4
        self.assertIn('foo', Config)
        del Config['foo']
        self.assertNotIn('foo', Config)

    def test_keys(self):
        Config['foo'] = 4
        Config['bar'] = 6
        self.assertEqual(set(Config.keys()), set(['foo', 'bar']))

    def test_values(self):
        Config['foo'] = 4
        Config['bar'] = 6
        self.assertEqual(set(Config.values()), set([6, 4]))

    def test_items(self):
        Config['foo'] = 4
        Config['bar'] = 6
        self.assertEqual(set(Config.items()), set([('bar',6), ('foo',4)]))

    def test_setdefault(self):
        v = Config.setdefault('bar', 4)
        self.assertEqual(4, v)
        self.assertEqual(4, Config['bar'])

    def test_update(self):
        d = dict(a=5, foo='bar', z='car')
        Config.update(**d)
        self.assertEqual(d, dict(Config))

    def test_json(self):
        d = dict(a=5, foo='bar', z='car', zoo=False)
        Config.update(**d)
        self.assertEqual(d, Config.__json__())



    def _test_value(self, v):
        Config['foo'] = v
        self.assertIsInstance(Config['foo'], type(v))
        self.assertEqual(Config['foo'], v)

    def test_float(self):
        self._test_value(3.33333)

    def test_int(self):
        self._test_value(3)

    def test_unicode(self):
        self._test_value(u'Avión')

    def test_str(self):
        self._test_value('A')

    def test_bool(self):
        self._test_value(True)
        self._test_value(False)

    def test_invalid_type(self):
        self.assertRaises(TypeError, Config.__setitem__, 'foo', {})
