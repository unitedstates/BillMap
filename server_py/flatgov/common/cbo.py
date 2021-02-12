#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, argparse, logging, re, json, gzip
from typing import Dict
from functools import reduce

from common import constants, utils
from bills.models import Bill, Sponsor

import xmltodict


logging.basicConfig(filename='billdata.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def logName(dirName: str, fileName: str):
  """
  Prints the name provided (path to a file to be processed) to the log.

  Args:
      fname (str): path of file to be processed 
  """

  logger.info('In directory: \t%s' % dirName)
  logger.info('Processing: \t%s' % fileName)

def getBillFromDirname(dirName: str) -> str:
  """
  Dirname is of the form ../../congress/data/116/bills/s/s245
  Want to retrieve the part that is 116/bills/s/s3583
  And return 116s3583

  Args:
     dirName (str): path to match 
  Returns:
     str: name of the bill (billCongressTypeNumber) 
  """
  m = constants.BILL_DIR_REGEX_COMPILED.match(dirName)
  if m and m.groups():
    return ''.join(list(m.groups()))
  else:
    return '' 
  

def getTopBillLevel(dirName: str):
  """
  Get path for the top level of a bill, e.g. ../../congress/data/116/bills/hr/hr1

  Args:
      dirName (str): path to match 

  Returns:
      [bool]: True if path is a top level (which will contain data.json); False otherwise  
  """
  dirName_parts = dirName.split('/')
  return (re.match(r'[a-z]+[0-9]+', dirName_parts[-1]) is not None and dirName_parts[-3]=='bills')

def isDataXML(fileName: str) -> bool:
  return fileName == 'fdsys_billstatus.xml'

def rec_cbo_item(cbo_items):
  #print(cbo_items)
  #quit()
  print('-----')
  for cbo_item in cbo_items:
    if type(cbo_item) is not str:
      #print(cbo_item)
      rec_cbo_item(cbo_item)
      
    else:
      print(cbo_item)
      print(cbo_items[cbo_item])


def collect_cbo_data_into_json(rootDir = constants.PATH_TO_CONGRESSDATA_DIR, processFile = logName, dirMatch = getTopBillLevel, fileMatch = isDataXML):
    for dirName, subdirList, fileList in os.walk(rootDir):
      if dirMatch(dirName):
        #logger.info('Entering directory: %s' % dirName)
        filteredFileList = [fitem for fitem in fileList if fileMatch(fitem)]
        for fname in filteredFileList:
          #print(dirName+fname)
          cbo_file = dirName+'/'+fname
          with open(cbo_file) as xml_file:
            data = xmltodict.parse(xml_file.read())
          #print(data.keys())
          bill_status = data['billStatus']
          #print(bill_status.keys())
          bill = bill_status['bill']
          #print(bill.keys())
          cbo_cost_estimates = bill['cboCostEstimates']
          if cbo_cost_estimates:

            cbo_items = cbo_cost_estimates['item']
            #print('-------', cbo_items)
            rec_cbo_item(cbo_items)
            #for cbo_item in cbo_items:
              #print('-----------', type(cbo_item))


          #quit()
            #processFile(dirName=dirName, fileName=fname)
          

def cbo():
  collect_cbo_data_into_json()




