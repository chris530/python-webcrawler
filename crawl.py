#!/usr/bin/env python

import requests
import Queue
import re
from BeautifulSoup import BeautifulSoup
import time

DOMAIN = "openai.com"

visited = {}
q = Queue.Queue()

def standardize_url(url, PASS_DOMAIN=None):
   '''just makes sures your is always the same, takes off www etc'''

   if PASS_DOMAIN is None:
      use_domain = DOMAIN
   else:
      use_domain = PASS_DOMAIN[0]

   # Fix to not follow redirects
   url = url.split("?")[0] 

   if url is None or False:
     return DOMAIN

   if re.search("^/",url):
     return use_domain + url

   if re.search("{}".format(DOMAIN),url):
     # Makes sures the domain is in the url
     pass
   else:
     return DOMAIN

   if re.search("^https://",url):
    if re.search("^https://www.",url):
  
      # for simplicity,  lets make sure all urls are https://*.use_domain
      return re.sub("\.www\.","", url).strip("/")

    else:
      return url.strip("/")

   elif re.search("^http://",url):
     if re.search("^http://www.",url):
     
       return re.sub("http://www\.","https://", url).strip("/")
   
     elif re.search("^http://",url):
       return re.sub("^http","https", url).strip("/")

     else:
       return False

   elif re.search("^www\.",url):
     return re.sub("^www\.","",url)  

   else:
     return "https://" + url

def visit_url(url):

   for _ in return_all_links(url):

     if re.search("^/",_):
       domain = re.findall("https://[a-zA-Z0-9\.]*{}".format(DOMAIN), url) 
       std_url = standardize_url(_,PASS_DOMAIN=domain)
       q.put(std_url)
 
     else:
 
       std_url = standardize_url(_)
       q.put(std_url)

def return_all_links(url):

  sites = []
 
  try:
    soup = BeautifulSoup(requests.get(standardize_url(url)).text)
    for link in soup.findAll('a'):
   
      linkpass = link.get('href')

      if re.search("^/", linkpass):
        domain = re.findall("https://[a-zA-Z0-9\.]*{}".format(DOMAIN), url)
        sites.append(standardize_url(linkpass,PASS_DOMAIN=domain))
      else:
        sites.append(standardize_url(linkpass))

    return sites
  except:
    return []  

# Start program

if __name__ == '__main__':

  q.put(DOMAIN)
 
  while not q.empty():
 
    site = q.get()

    if visited.has_key(site):
      continue
 
    print "Visiting",site
    visit_url(standardize_url(site))
    visited.update({site: True})
