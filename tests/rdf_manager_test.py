# rdf_manager_test.py - unit tests for pynappl rdf manager
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

import unittest
import pynappl
import os, os.path
from file_manager_test import FileManagerTestCase


class RecordingStore(pynappl.Store):
  """An instrumented version of Store that records calls to  store_file"""
  
  def __init__(self):
    pynappl.Store.__init__(self, 'http://example.com/recordingstore')
    self.files_processed = []
  
  def store_file(self, filename):
    self.files_processed.append(filename)


class ProcessFileTestCase(FileManagerTestCase):
  
  def test_list_non_recursive_empty_dir(self):
    self.add_file('foo')
    self.add_file('bar')

    store = RecordingStore()
    m = pynappl.RDFManager(store, self.dirname, False)
    m.process()

    self.assertEqual( 2, len(store.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in store.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'bar') in store.files_processed )


