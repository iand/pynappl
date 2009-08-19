# file_manager_test.py - unit tests for pynappl rdf manager
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
import tempfile
from mock_store import MockStore
import os, os.path


class FileManagerTestCase(unittest.TestCase):
  def setUp(self):
    self.dirname = tempfile.mkdtemp()
  
  def tearDown(self):
    for root, dirs, files in os.walk(self.dirname, topdown=False):
      for name in files:
          os.remove(os.path.join(root, name))
      for name in dirs:
          os.rmdir(os.path.join(root, name))
    os.rmdir(self.dirname)
    
  def add_file(self, filename, data='dummy data'):
    file = open(os.path.join(self.dirname, filename), 'w')
    file.write(data)
    file.close()
    
  def add_dir(self, dirname):
    os.mkdir(os.path.join(self.dirname, dirname))

class ListTestCase(FileManagerTestCase):
  
  def test_list_non_recursive_empty_dir(self):
    m = pynappl.FileManager(self.dirname, False)
    files = m.list()
    self.assertEqual(0, len(files))

  def test_list_non_recursive_populated_dir(self):
    self.add_file('foo')
    self.add_file('bar')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_non_recursive_ignores_ok_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.ok')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_non_recursive_ignores_fail_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.fail')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_non_recursive_uses_filename_filter(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('bar.rdf.fail')
    self.add_file('bar.rdf')
    self.add_file('dir1/baz.rdf')
    m = pynappl.FileManager(self.dirname, False, '\.rdf$')
    files = m.list()
    self.assertEqual(1, len(files))


  def test_list_recursive_empty_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list()
    self.assertEqual(0, len(files))

  def test_list_recursive_populated_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('dir1/foo1')
    self.add_file('dir2/foo2')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list()
    self.assertEqual(4, len(files))

  def test_list_recursive_ignores_ok_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.ok')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_recursive_ignores_fail_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.fail')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_recursive_uses_filename_filter(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('bar.rdf.fail')
    self.add_file('bar.rdf')
    self.add_file('dir1/baz.rdf')
    m = pynappl.FileManager(self.dirname, True, '\.rdf$')
    files = m.list()
    self.assertEqual(2, len(files))


class ListNewTestCase(FileManagerTestCase):
  
  def test_list_new_non_recursive_empty_dir(self):
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_new()
    self.assertEqual(0, len(files))

  def test_list_new_non_recursive_populated_dir(self):
    self.add_file('foo')
    self.add_file('bar')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_new()
    self.assertEqual(2, len(files))

  def test_list_new_non_recursive_ignores_ok_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.ok')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_new()
    self.assertEqual(1, len(files))

  def test_list_new_non_recursive_ignores_fail_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.fail')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_new()
    self.assertEqual(1, len(files))

  def test_list_new_recursive_empty_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_new()
    self.assertEqual(0, len(files))

  def test_list_new_recursive_populated_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('dir1/foo1')
    self.add_file('dir2/foo2')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_new()
    self.assertEqual(4, len(files))

  def test_list_new_recursive_ignores_ok_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.ok')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_new()
    self.assertEqual(1, len(files))

  def test_list_new_recursive_ignores_fail_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.fail')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_new()
    self.assertEqual(1, len(files))


class RecordingFileManager(pynappl.FileManager):
  """An instrumented version of FileManager that records which files were processed"""
  
  def __init__(self, directory_name, recursive= False, filename_filter = None, ok_suffix='ok', fail_suffix='fail'):
    pynappl.FileManager.__init__(self, directory_name, recursive, filename_filter, ok_suffix, fail_suffix)
    self.files_processed = []
  
  def process_file(self, filename):
    self.files_processed.append(filename)

class FailingFileManager(pynappl.FileManager):
  """An instrumented version of FileManager that always fails to process a file"""
  
  def __init__(self, directory_name, recursive= False, filename_filter = None, ok_suffix='ok', fail_suffix='fail'):
    pynappl.FileManager.__init__(self, directory_name, recursive, filename_filter, ok_suffix, fail_suffix)
    self.files_processed = []
  
  def process_file(self, filename):
    self.files_processed.append(filename)
    return "%s failed" % filename

class SucceedingFileManager(pynappl.FileManager):
  """An instrumented version of FileManager that always succeeds processing a file"""
  
  def __init__(self, directory_name, recursive= False, filename_filter = None, ok_suffix='ok', fail_suffix='fail'):
    pynappl.FileManager.__init__(self, directory_name, recursive, filename_filter, ok_suffix, fail_suffix)
    self.files_processed = []
  
  def process_file(self, filename):
    self.files_processed.append(filename)
    return ""

class ProcessTestCase(FileManagerTestCase):

  def test_process_non_recursive_passes_all_files_to_process_file(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    m = RecordingFileManager(self.dirname, False)
    m.process()
    self.assertEqual( 2, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'bar') in m.files_processed )
    self.assertFalse( os.path.join(self.dirname, 'dir1/baz') in m.files_processed )

  def test_process_recursive_passes_all_files_to_process_file(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    m = RecordingFileManager(self.dirname, True)
    m.process()
    self.assertEqual( 3, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'bar') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'dir1/baz') in m.files_processed )

  def test_process_writes_fail_file(self):
    self.add_file('foo')
    m = FailingFileManager(self.dirname, False)
    m.process()
    self.assertEqual( 1, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'foo.fail')) )
    f = open(os.path.join(self.dirname, 'foo.fail'), "r")
    self.assertEqual( "%s failed" % os.path.join(self.dirname, 'foo'), f.read())
    f.close()
  
  def test_process_writes_ok_file(self):
    self.add_file('foo')
    m = SucceedingFileManager(self.dirname, False)
    m.process()
    self.assertEqual( 1, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'foo.ok')) )
    f = open(os.path.join(self.dirname, 'foo.ok'), "r")
    self.assertEqual( "OK", f.read())
    f.close()

  def test_process_writes_fail_file_recursive(self):
    self.add_file('foo')
    self.add_dir('bar')
    self.add_file('bar/spam')
    m = FailingFileManager(self.dirname, True)
    m.process()
    self.assertEqual( 2, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'bar/spam') in m.files_processed )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'foo.fail')) )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'bar/spam.fail')) )
    f = open(os.path.join(self.dirname, 'foo.fail'), "r")
    self.assertEqual( "%s failed" % os.path.join(self.dirname, 'foo'), f.read())
    f.close()
    f = open(os.path.join(self.dirname, 'bar/spam.fail'), "r")
    self.assertEqual( "%s failed" % os.path.join(self.dirname, 'bar/spam'), f.read())
    f.close()
  
  def test_process_writes_ok_file_recursive(self):
    self.add_file('foo')
    self.add_dir('bar')
    self.add_file('bar/spam')
    m = SucceedingFileManager(self.dirname, True)
    m.process()
    self.assertEqual( 2, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'bar/spam') in m.files_processed )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'foo.ok')) )
    self.assertTrue( os.path.exists(os.path.join(self.dirname, 'bar/spam.ok')) )
    f = open(os.path.join(self.dirname, 'foo.ok'), "r")
    self.assertEqual( "OK", f.read())
    f.close()
    f = open(os.path.join(self.dirname, 'bar/spam.ok'), "r")
    self.assertEqual( "OK", f.read())
    f.close()

class ListFailuresTestCase(FileManagerTestCase):

  def test_list_failures_non_recursive(self):
    self.add_file('foo')
    self.add_file('foo.ok')
    self.add_file('bar')
    self.add_file('bar.fail')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.fail')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_failures()
    self.assertEqual( 1, len(files) )
    self.assertFalse( os.path.join(self.dirname, 'foo') in files )
    self.assertTrue( os.path.join(self.dirname, 'bar') in files )
    self.assertFalse( os.path.join(self.dirname, 'dir1/baz') in files )

  def test_list_failures_recursive(self):
    self.add_file('foo')
    self.add_file('foo.ok')
    self.add_file('bar')
    self.add_file('bar.fail')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.fail')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_failures()
    self.assertEqual( 2, len(files) )
    self.assertFalse( os.path.join(self.dirname, 'foo') in files )
    self.assertTrue( os.path.join(self.dirname, 'bar') in files )
    self.assertTrue( os.path.join(self.dirname, 'dir1/baz') in files )

class ListSuccessesTestCase(FileManagerTestCase):

  def test_list_successes_non_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_successes()
    self.assertEqual( 1, len(files) )
    self.assertFalse( os.path.join(self.dirname, 'foo') in files )
    self.assertTrue( os.path.join(self.dirname, 'bar') in files )
    self.assertFalse( os.path.join(self.dirname, 'dir1/baz') in files )

  def test_list_successes_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_successes()
    self.assertEqual( 2, len(files) )
    self.assertFalse( os.path.join(self.dirname, 'foo') in files )
    self.assertTrue( os.path.join(self.dirname, 'bar') in files )
    self.assertTrue( os.path.join(self.dirname, 'dir1/baz') in files )


class SummaryTestCase(FileManagerTestCase):

  def test_summary_non_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, False)
    summary = m.summary()
    self.assertEqual( self.dirname  + " contains 2 files: 1 failed, 1 succeeded, 0 new", summary )

  def test_successes_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, True)
    summary = m.summary()
    self.assertEqual( self.dirname  + " contains 3 files: 1 failed, 2 succeeded, 0 new", summary )


class ResetTestCase(FileManagerTestCase):

  def test_reset_non_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, False)
    files = m.list_new()
    self.assertEqual(0, len(files) )
    m.reset()
    files = m.list_new()
    self.assertEqual(2, len(files) )

  def test_reset_recursive(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.ok')
    m = pynappl.FileManager(self.dirname, True)
    files = m.list_new()
    self.assertEqual(0, len(files) )
    m.reset()
    files = m.list_new()
    self.assertEqual(3, len(files) )

class RetryFailuresTestCase(FileManagerTestCase):

  def test_retry_failures_non_recursive_passes_all_files_to_process_file(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.fail')
    m = RecordingFileManager(self.dirname, False)
    m.retry_failures()
    self.assertEqual( 1, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertFalse( os.path.join(self.dirname, 'bar') in m.files_processed )
    self.assertFalse( os.path.join(self.dirname, 'dir1/baz') in m.files_processed )


  def test_retry_failures_recursive_passes_all_files_to_process_file(self):
    self.add_file('foo')
    self.add_file('foo.fail')
    self.add_file('bar')
    self.add_file('bar.ok')
    self.add_dir('dir1')
    self.add_file('dir1/baz')
    self.add_file('dir1/baz.fail')
    m = RecordingFileManager(self.dirname, True)
    m.retry_failures()
    self.assertEqual( 2, len(m.files_processed) )
    self.assertTrue( os.path.join(self.dirname, 'foo') in m.files_processed )
    self.assertFalse( os.path.join(self.dirname, 'bar') in m.files_processed )
    self.assertTrue( os.path.join(self.dirname, 'dir1/baz') in m.files_processed )

if __name__ == "__main__":
  unittest.main()


