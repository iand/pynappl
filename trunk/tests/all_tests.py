#!/usr/bin/env python

import unittest
import store_test


def suite():
  suite1 = unittest.TestLoader().loadTestsFromTestCase(store_test.BuildUri)
  return unittest.TestSuite([suite1])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

