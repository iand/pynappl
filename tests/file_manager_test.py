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

class ListTestCase(unittest.TestCase):
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

  
  def test_list_non_recursive_empty_dir(self):
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list()
    self.assertEqual(0, len(files))

  def test_list_non_recursive_populated_dir(self):
    self.add_file('foo')
    self.add_file('bar')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_non_recursive_ignores_ok_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.ok')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_non_recursive_ignores_fail_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.fail')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list()
    self.assertEqual(2, len(files))

  def test_list_recursive_empty_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list(True)
    self.assertEqual(0, len(files))

  def test_list_recursive_populated_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('dir1/foo1')
    self.add_file('dir2/foo2')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list(True)
    self.assertEqual(4, len(files))

  def test_list_recursive_ignores_ok_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.ok')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list(True)
    self.assertEqual(2, len(files))

  def test_list_recursive_ignores_fail_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.fail')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list(True)
    self.assertEqual(2, len(files))



class ListNewTestCase(unittest.TestCase):
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

  
  def test_list_new_non_recursive_empty_dir(self):
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new()
    self.assertEqual(0, len(files))

  def test_list_new_non_recursive_populated_dir(self):
    self.add_file('foo')
    self.add_file('bar')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new()
    self.assertEqual(2, len(files))

  def test_list_new_non_recursive_ignores_ok_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.ok')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new()
    self.assertEqual(1, len(files))

  def test_list_new_non_recursive_ignores_fail_suffix(self):
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('bar.fail')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new()
    self.assertEqual(1, len(files))

  def test_list_new_recursive_empty_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new(True)
    self.assertEqual(0, len(files))

  def test_list_new_recursive_populated_dir(self):
    self.add_dir('dir1')
    self.add_dir('dir2')
    self.add_file('foo')
    self.add_file('bar')
    self.add_file('dir1/foo1')
    self.add_file('dir2/foo2')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new(True)
    self.assertEqual(4, len(files))

  def test_list_new_recursive_ignores_ok_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.ok')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new(True)
    self.assertEqual(1, len(files))

  def test_list_new_recursive_ignores_fail_suffix(self):
    self.add_dir('dir1')
    self.add_file('foo')
    self.add_file('dir1/bar')
    self.add_file('dir1/bar.fail')
    m = pynappl.FileManager(MockStore(), self.dirname)
    files = m.list_new(True)
    self.assertEqual(1, len(files))


if __name__ == "__main__":
  unittest.main()


