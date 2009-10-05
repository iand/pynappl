import unittest
import pynappl
class EntityMatcherTestCase(unittest.TestCase):
	def test_looks_up_name(self):
		name = "Africa"
		e = pynappl.EntityMatcher()
		uri = e.lookup(name)
		self.assertEqual(uri, "http://sws.geonames.org/6255146/")
if __name__ == "__main__":
	unittest.main()
