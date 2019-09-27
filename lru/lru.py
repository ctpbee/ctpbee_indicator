__version__ = '0.1'

class LRUCache(object):
    def __init__(self, max_items=100):
        self.cache = {}
        self.key_order = []
        self.max_items = max_items

    def __setitem__(self, key, value):
        self.cache[key] = value
        self._mark(key)

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            # Explicit reraise for better tracebacks
            raise KeyError
        self._mark(key)
        return value 

    def _mark(self, key):
        if key in self.key_order:
            self.key_order.remove(key)

        self.key_order.insert(0, key)
        if len(self.key_order) > self.max_items:
            remove = self.key_order[self.max_items]
            del self.cache[remove]
            self.key_order.remove(remove)

if __name__ == '__main__':
    import unittest

    class TestCase(unittest.TestCase):
        def test_cache(self):
            cache = LRUCache(max_items=2)
            cache['foo'] = 1
            cache['bar'] = 10
            cache['baz'] = 100

            self.assertRaises(KeyError, cache.__getitem__, 'foo')
            self.assertEqual(cache['bar'], 10)
            self.assertEqual(cache['baz'], 100)

    unittest.main()
