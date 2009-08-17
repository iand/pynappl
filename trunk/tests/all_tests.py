#!/usr/bin/env python

import unittest
import store_test
import job_test


def suite():
  return unittest.TestSuite([
                              unittest.TestLoader().loadTestsFromTestCase(store_test.BuildUriTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.DescribeTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ScheduleResetTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ScheduleSnapshotTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ScheduleReindexTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ScheduleRestoreTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.ReadJobTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.StoreDataTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(job_test.ParseTestCase)
                            ])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

