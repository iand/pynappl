#!/usr/bin/env python
# all_tests.py - runs all unit tests in pynappl package
# Copyright (C) 2009 Talis Information Ltd.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import sys; sys.path.insert(0, "/home/kier/newrdflib")

import unittest
import store_test
import job_test
import file_manager_test
import rdf_manager_test
import store_config_test
import entitymatcher_test

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
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.StoreFileTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.StoreGraphTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.StoreUrlTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.AuthenticationTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.UriTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.AccessStatusTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.SparqlTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.SearchTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.SnapshotsTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.FpmapTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_test.QueryProfileTestCase)


                            , unittest.TestLoader().loadTestsFromTestCase(job_test.ParseTestCase)

                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ListTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ListNewTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ProcessTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ProcessCallbackTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ListFailuresTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ListSuccessesTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.SummaryTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.ResetTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(file_manager_test.RetryFailuresTestCase)

                            , unittest.TestLoader().loadTestsFromTestCase(rdf_manager_test.ProcessFileTestCase)

                            , unittest.TestLoader().loadTestsFromTestCase(store_config_test.StoreConfigTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_config_test.FPMapTestCase)
                            , unittest.TestLoader().loadTestsFromTestCase(store_config_test.QueryProfileTestCase)
                            
                            , unittest.TestLoader().loadTestsFromTestCase(entitymatcher_test.EntityMatcherTestCase)
                            ])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

