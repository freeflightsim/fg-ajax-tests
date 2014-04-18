#!/usr/bin/env python


import json
import urllib
import urllib2


ajax_url = "http://localhost:9999/json/" #server + base_url

print ajax_url

response = urllib2.urlopen(ajax_url)
content = response.read()

print content

data = json.loads(content)
print data

print data['nChildren']


