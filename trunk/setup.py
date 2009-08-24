#!/usr/bin/python
# Copyright (C) 2009 Talis Information Ltd.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	02110-1301 USA

import sys
from distutils.core import setup

required = []
version = '0.1.0'

setup(
		name='pynappl',
		version=version,
		description='Python client library for the Talis Platform',
		long_description = """Pynappl makes it easy to interact with Talis Platform services through the Google Data APIs.""",
		author='Ian Davis',
		author_email='nospam@iandavis.com',
		license='GPL2',
		url='http://code.google.com/p/pynappl/',
		packages=['pynappl'],
		package_dir = {'pynappl':'src/pynappl'},
		scripts=['bin/tstore', 'samples/numtriples.py', 'samples/rdfvalidate.py'],
		install_requires=required,
		)
