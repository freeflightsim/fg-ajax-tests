#!/usr/bin/env python


import json
import urllib
import urllib2

server = "http://localhost:9999"


base_url = "/json/"

url = server + base_url

print url
#user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#headers = { 'User-Agent' : user_agent }

headers = {}

values = {}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page
