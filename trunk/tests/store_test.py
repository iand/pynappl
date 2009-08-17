import unittest
import pynappl

class BuildUri(unittest.TestCase):

  def test_build_uri_abs(self):
    """build_uri returns absolute URIs if they are in store's URI space"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('http://example.com/store/foo'))

  def test_build_uri_rel(self):
    """build_uri appends relative URIs to the store URI"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('/foo'))

  def test_build_uri_rel_slashless(self):
    """build_uri ensures relative URIs are appended with a slash"""
    store = pynappl.Store('http://example.com/store')
    self.assertEqual('http://example.com/store/foo', store.build_uri('foo'))
    


if __name__ == "__main__":
    unittest.main()


