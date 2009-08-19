# file_manager.py - base class for managing a directory of files
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

__all__ = ["FileManager", "file_manager_main"]

import pynappl
import os
import re

class FileManager():
  def __init__(self, directory_name, recursive = False, filename_filter = None, ok_suffix='ok', fail_suffix='fail', callback=None):
    self.dirname = directory_name
    self.ok_suffix = ok_suffix
    self.fail_suffix = fail_suffix
    self.recursive = recursive
    if filename_filter is not None:
      self.filename_filter = re.compile(filename_filter)
    else:
      self.filename_filter = None
    self.callback = callback
    
  def process(self):
    """Process all files in directory"""
    for filename in self.list_new():
      res = self.process_file(filename)
      if res:
        f = open(self.fail_filename(filename), "w")
        f.write(res)
        f.close()
      else:
        f = open(self.ok_filename(filename), "w")
        f.write("OK")
        f.close()

  def list(self): 
    """List all files in directory that do not end with ok_suffix or fail_suffix"""
    files = []
    if self.recursive:
      for root, dirs, files_found in os.walk(self.dirname):
        for filename in files_found:
          full_filename = os.path.join(root, filename)
          if os.path.isfile(full_filename) and not full_filename.endswith("." + self.ok_suffix) and not full_filename.endswith("." + self.fail_suffix):
            if self.filename_filter is None or self.filename_filter.search(full_filename, re.IGNORECASE) is not None:
              files.append(full_filename)
    else:
      for filename in os.listdir(self.dirname):
        full_filename = os.path.join(self.dirname, filename)
        if os.path.isfile(full_filename) and not full_filename.endswith("." + self.ok_suffix) and not full_filename.endswith("." + self.fail_suffix):
          if self.filename_filter is None or self.filename_filter.search(full_filename, re.IGNORECASE) is not None:
            files.append(full_filename)
    

    return files

  def list_new(self):
    """List all files in directory that don't have a ok or fail file"""
    files = []
    for filename in self.list():
      ok_filename = self.ok_filename(filename)
      fail_filename = self.fail_filename(filename)
      if not os.path.exists(ok_filename) and not os.path.exists(fail_filename):
        files.append(filename)

    return files

  def ok_filename(self, filename):
    return filename + '.' + self.ok_suffix

  def fail_filename(self, filename):
    return filename + '.' + self.fail_suffix
    
  def process_file(self, filename):
    if self.callback is not None:
      return self.callback(filename)
  
  def list_failures(self):
    """List all files marked as failing"""
    files = []
    for filename in self.list():
      if os.path.exists(self.fail_filename(filename)):
        files.append(filename)

    return files
    
  def list_successes(self):
    """List all files marked as ok"""
    files = []
    for filename in self.list():
      if os.path.exists(self.ok_filename(filename)):
        files.append(filename)

    return files
    
  def summary(self):
    """Produce a summary of progress"""
    new = self.list_new()
    failures = self.list_failures()
    successes = self.list_successes()
    total = len(new) + len(failures) + len(successes)

    return "%s contains %s files: %s failed, %s succeeded, %s new" % (self.dirname, total, len(failures), len(successes), len(new))
  
  def reset(self):
    """Remove all failure and success files"""
    files = []
    if self.recursive:
      for root, dirs, files_found in os.walk(self.dirname):
        for filename in files_found:
          full_filename = os.path.join(root, filename)
          if os.path.isfile(full_filename) and (full_filename.endswith("." + self.ok_suffix) or full_filename.endswith("." + self.fail_suffix)):
            os.remove(full_filename)
    else:
      for filename in os.listdir(self.dirname):
        full_filename = os.path.join(self.dirname, filename)
        if os.path.isfile(full_filename) and (full_filename.endswith("." + self.ok_suffix) or full_filename.endswith("." + self.fail_suffix)):
          os.remove(full_filename)
    
    
  def retry_failures(self):
    """Process all files marked as failure in directory"""
    for filename in self.list_failures():
      os.remove(self.fail_filename(filename))
      self.process_file(filename)

class PrintingFileManager(FileManager):
  def process_file(self, filename):
    print "Processing '%s'" % filename

def file_manager_main(cls=FileManager, callback=None):
  import sys, getopt
  directory = os.getcwd()
  action = "process"
  recursive = False
  filter = None
  ok_suffix = "ok"
  fail_suffix = "fail"
  opts, args = getopt.gnu_getopt(sys.argv[1:], "d:a:rF:o:f:", ["directory=", "action=", "recursive", "filter=", "ok-suffix=", "fail-suffix="])
  for k, v in opts:
    if k in ("-d", "--directory"):
      directory = v
    elif k in ("-a", "--action"):
      if v in ["process", "list", "list-new", "list-failures", "list-successes", "summary", "reset", "retry-failures"]:
         action = v.replace("-", "_")
    elif k in ("-r", "--recursive"):
      recursive = True
    elif k in ("-F", "--filter"):
      filter = v
    elif k in ("-o", "--ok-suffix"):
      ok_suffix = v
    elif k in ("-f", "--fail-suffix"):
      fail_suffix = v
  fm = cls(directory, recursive, filter, ok_suffix, fail_suffix, callback)
  res = getattr(fm, action)()
  if isinstance(res, list):
    for item in res:
      print item
  elif res is not None:
    print res
if __name__ == "__main__":
  file_manager_main(PrintingFileManager)
