#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, logging, re
from typing import Dict
from functools import reduce

from common import constants, utils
from bills.models import CboReport

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
  #print('-----')
  cbo = {}
  
  for cbo_item in cbo_items:
    if type(cbo_item) is not str:
      #print(cbo_item)
      rec_cbo_item(cbo_item)
      
    else:
      #print(cbo_item)
      #print(cbo_items[cbo_item])
      cbo[cbo_item] = cbo_items[cbo_item]

  return cbo


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
            cbo_data = rec_cbo_item(cbo_items)
            #print(cbo_data)
            save_cbo_data_to_db(cbo_data)
            #print('------------------', rec_cbo_item(cbo_items))
            #for cbo_item in cbo_items:
              #print('-----------', type(cbo_item))


          #quit()
            #processFile(dirName=dirName, fileName=fname)

def save_cbo_data_to_db(cbo_data):
  
  try:
    cbo = {}
    pub_date = cbo_data['pubDate']
    title = cbo_data['title']
    url = cbo_data['url']
    bill_number = title.split(',')
    splited = ''.join(bill_number[0].split('.'))
    splited = ''.join(splited.split(' '))
    of_split = splited.split('of')[-1]
    or_split = of_split.split('or')[-1]
    bill_number = or_split
    date = pub_date.split('T')[0]
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    congress = 0
    #print(day)
    const_year = 2022
    const_congress = 117
    dif = const_year - int(year)
    congress = const_congress - (dif // 2)
    cbo['pub_date'] = date
    cbo['title'] = title
    cbo['original_pdf_link'] = url
    cbo['bill_number'] = bill_number
    cbo['congress'] = congress
    #print(cbo)

    queryset_cbo = CboReport.objects.filter(
      bill_number=cbo['bill_number'],
      bill_id=str(cbo['congress']) + str(cbo['bill_number']).lower(),
      congress=cbo['congress']
    )

    if not queryset_cbo.exists():
      cboreport = CboReport()
      cboreport.pub_date = cbo['pub_date']
      cboreport.title = cbo['title']
      cboreport.original_pdf_link = cbo['original_pdf_link']
      cboreport.bill_id = str(cbo['congress']) + str(cbo['bill_number']).lower()
      cboreport.bill_number = cbo['bill_number']
      cboreport.congress = cbo['congress']
      print(str(congress) + ': ' + str(cbo['title']))
      cboreport.save()


  except Exception as e:
    #print("------------------------------------ COULDN'T SAVE ---------------------------------------")
    #print(cbo_data)
    print('-------- ERROR --------', e)
    pass

def cbo():
  collect_cbo_data_into_json()




