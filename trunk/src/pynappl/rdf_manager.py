# rdf_manager.py - manages a directory of rdf files
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

__all__ = ["RDFManager"]

import pynappl

class RDFManager(pynappl.FileManager):
  def __init__(self, store, directory_name, recursive = False, filename_filter = None, ok_suffix='ok', fail_suffix='fail'):
    pynappl.FileManager.__init__(self, directory_name, recursive, filename_filter, ok_suffix, fail_suffix)
    self.store = store
    
  def process_file(self, filename):
    self.store.store_file(filename)
