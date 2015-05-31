#!/usr/bin/python

from urlparse import urlparse
import csv
import pythonwhois

from multiprocessing import Pool
from time import sleep
from random import randint
import os
import pickle

class AsyncFactory:
    def __init__(self, func, cb_func):
        self.func = func
        self.cb_func = cb_func
        self.pool = Pool(processes=100)

    def call(self,*args, **kwargs):
        self.pool.apply_async(self.func, args, kwargs, self.cb_func)

    def wait(self):
        self.pool.close()
        self.pool.join()

allDict = pickle.load( open( "dict.p", "rb" ) )
def cb_func(x):
    print "+"
    allDict[x[0]] = x[1]

def whois(who,cnt):
  if cnt == 0:
    domain = pythonwhois.get_whois(who)
    for key in domain.keys():
      obj = domain[key]
      if type(obj) is dict:
        cnt = cnt + 1
        cnt = cnt + whois(obj,cnt)
      else:
        cnt = cnt + 1
    return [who,cnt]
  else:
    for key in who.keys():
      obj = who[key]
      if type(obj) is dict:
        cnt = cnt + 1
        cnt = cnt + whois(obj,cnt)
      else:
        cnt = cnt + 1
    return cnt


with open('allDataSet.csv', 'rb') as csvfile:
  async_queue = AsyncFactory(whois, cb_func)
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  next(reader,None)
   
  with open('test1.csv','w') as writefile:
    writer = csv.writer(writefile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Id','Time','Url','Ip','Malware','Country','Url_length','Is_Sub_Domain','Who_is_score'])
    for row in reader:
      url = row[2]
      #parsed url
      urlp = urlparse('//'+url)
      #first property
      url_length = len(url)
      row.append(url_length)
    
      #isSubDomain?
      isSubDomain = 1
      subd = urlp.netloc
      subd = subd.split('.')
      if len(subd) > 1:
        isSubDomain = len(subd)
      row.append(isSubDomain)  
     

      #whoisRecord
      whoisurl = urlp.netloc
      whoisurl = whoisurl[1:-1]
      whoisscore = allDict.get(whoisurl,0)

      """
      try:
        async_queue.call(whoisurl,0)
        #whoisscore = whois(whoisurl,0)
        #print '+'
      except (pythonwhois.shared.WhoisException,KeyError) as e:
        print "whois exception " + whoisurl
        pass
      """
      row.append(whoisscore)
      writer.writerow(row)
  
  async_queue.wait()
  #pickle.dump( allDict, open( "dict.p", "wb" ) )
