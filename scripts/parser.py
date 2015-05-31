#!/usr/bin/python

import socket
import csv

from urllib2 import urlopen
from contextlib import closing
import json
from time import gmtime, strftime


# Ip to Country Code function
def ip_to_co(ip):
  url = 'http://freegeoip.net/json/'
  try:
      temp = url + ip
      with closing(urlopen(temp)) as response:
          location = json.loads(response.read())
          location_code = location['country_code']
          return location_code
  except:
      print("Location could not be determined automatically")
      return "NA"




with open('alexa_1000_sampled.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(reader,None)

  with open('alexa_1000_ip.csv','w') as writefile:
    writer = csv.writer(writefile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
      str = ''.join(row).split(',')[2][1:-1]
      try:
        ip  = socket.gethostbyname(str)
        code = ip_to_co(ip)
        time = strftime("%Y/%m/%d_%H:%M", gmtime())
        print str + ' ' + ip + ' ' + code
        list = [time,str,ip,'No',code]
        writer.writerow(list)
      except socket.gaierror:
        print "Exception"
