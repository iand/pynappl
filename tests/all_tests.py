#!/usr/bin/env python

import unittest
import store_test


def suite():
  return unittest.TestSuite([
                              unittest.TestLoader().loadTestsFromTestCase(store_test.BuildUriTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.DescribeTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ScheduleResetTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ReadJobTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.StoreDataTestCase)
                            ])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

