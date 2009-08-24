# store_config.py - class representing Talis Platform store configuration
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

__all__ = ["StoreConfig"]
import re

class StoreConfig:
		def __init__(self, uri):
			self.uri = uri

		def get_first_fpmap_uri(self):
			matches = re.match(r"^http:\/\/api\.talis\.com\/stores\/([a-z][a-zA-Z0-9-]+)\/config$", self.uri)
			if matches is not None:
				store_name = matches.group(1);    
    
				# special cases for very very early stores
				if store_name in ['ajmg-dev1','beobal-dev1', 'danja-dev1', 'dataMonitoring', 'iand-dev1', 'iand-dev2', 'iand-dev3', 'jingye-dev1', 'kwijibo-dev1', 'malcyl-dev1', 'quoll-dev1', 'schema-cache', 'silkworm-dev', 'silkworm', 'source-dev1', 'source-qa1', 'tomh-dev1']:
					return 'http://api.talis.com/stores/%s/indexes/default/fpmaps/default' % store_name
				elif ( re.search(r"^engage-dev\d+$", store_name) is not None
						or re.search(r"^engagetenant\d+$", store_name) is not None  
						or re.search(r"^list-demo\d+$", store_name) is not None 
						or re.search(r"^list-dev\d+$", store_name) is not None 
						or re.search(r"^list-qa\d+$", store_name) is not None  
						or re.search(r"^nuggetengage-demo\d+$", store_name) is not None    
						or re.search(r"^nuggetengage-qa\d+$", store_name) is not None 
						or re.search(r"^zephyr-cust\d+$", store_name) is not None    
						or store_name in ['engagetenantstore', 'list-tenants-dev']   ):
					return 'http://api.talis.com/stores/%s/indexes/metaboxIndex/fpmaps/fpmap' % store_name
				elif store_name in ['bib-sandbox', 'inst-5050', 'inst-u138', 'ukbib']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/fpmaps/fpmap' % store_name
				elif store_name in ['holdings']:
					return 'http://api.talis.com/stores/%s/indexes/m21Holdings/fpmaps/fpmap' % store_name
				elif store_name in ['union']:
					return 'http://api.talis.com/stores/%s/indexes/union/fpmaps/fpmap' % store_name
				elif store_name in ['wikipedia']:
					return 'http://api.talis.com/stores/%s/indexes/abstracts/fpmaps/fpmap' % store_name
				elif store_name in ['gatech']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/fpmap' % store_name
				elif store_name in ['cenotelist']:
					return 'http://api.talis.com/stores/%s/indexes/default/fpmaps/fpmap' % store_name
				elif store_name in ['image-sandbox']:
					return 'http://api.talis.com/stores/%s/indexes/image-sandbox/fpmaps/fpmap' % store_name
				elif store_name in ['cnimages']:
					return 'http://api.talis.com/stores/%s/indexes/cnimages/fpmaps/fpmap' % store_name
			return '%s/fpmaps/1' % self.uri
			
		def get_first_query_profile_uri(self):
			matches = re.match(r"^http:\/\/api\.talis\.com\/stores\/([a-z][a-zA-Z0-9-]+)\/config$", self.uri)
			if matches is not None:
				store_name = matches.group(1);    
    
				# special cases for very very early stores
				if store_name in ['ajmg-dev1','beobal-dev1', 'danja-dev1', 'dataMonitoring', 'iand-dev1', 'iand-dev2', 'iand-dev3', 'jingye-dev1', 'kwijibo-dev1', 'malcyl-dev1', 'quoll-dev1', 'schema-cache', 'silkworm-dev', 'silkworm', 'source-dev1', 'source-qa1', 'tomh-dev1']:
					return 'http://api.talis.com/stores/%s/indexes/default/queryprofiles/default' % store_name
				elif ( re.search(r"^engage-dev\d+$", store_name) is not None
						or re.search(r"^engagetenant\d+$", store_name) is not None  
						or re.search(r"^list-demo\d+$", store_name) is not None 
						or re.search(r"^list-dev\d+$", store_name) is not None 
						or re.search(r"^list-qa\d+$", store_name) is not None  
						or re.search(r"^nuggetengage-demo\d+$", store_name) is not None    
						or re.search(r"^nuggetengage-qa\d+$", store_name) is not None 
						or re.search(r"^zephyr-cust\d+$", store_name) is not None    
						or store_name in ['engagetenantstore', 'list-tenants-dev']   ):
					return 'http://api.talis.com/stores/%s/indexes/metaboxIndex/queryprofiles/default' % store_name
				elif store_name in ['bib-sandbox', 'inst-5050', 'inst-u138', 'ukbib']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/queryprofiles/default' % store_name
				elif store_name in ['holdings']:
					return 'http://api.talis.com/stores/%s/indexes/m21Holdings/queryprofiles/default' % store_name
				elif store_name in ['union']:
					return 'http://api.talis.com/stores/%s/indexes/union/queryprofiles/default' % store_name
				elif store_name in ['wikipedia']:
					return 'http://api.talis.com/stores/%s/indexes/abstracts/queryprofiles/default' % store_name
				elif store_name in ['gatech']:
					return 'http://api.talis.com/stores/%s/indexes/m21Advanced/queryprofiles/default' % store_name
				elif store_name in ['cenotelist']:
					return 'http://api.talis.com/stores/%s/indexes/default/queryprofiles/default' % store_name
				elif store_name in ['image-sandbox']:
					return 'http://api.talis.com/stores/%s/indexes/image-sandbox/queryprofiles/default' % store_name
				elif store_name in ['cnimages']:
					return 'http://api.talis.com/stores/%s/indexes/cnimages/queryprofiles/default' % store_name
			return '%s/queryprofiles/1' % self.uri
			
