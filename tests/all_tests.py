#!/usr/bin/env python

import unittest
import store_test


def suite():
  suite1 = unittest.TestLoader().loadTestsFromTestCase(store_test.BuildUriTestCase)
  suite2 = unittest.TestLoader().loadTestsFromTestCase(store_test.DescribeTestCase)
  return unittest.TestSuite([suite1, suite2])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

