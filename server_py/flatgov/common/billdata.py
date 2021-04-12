#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, argparse, logging, re, json, gzip
from typing import Dict
from functools import reduce
from bills.models import Bill

from common import constants, utils

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

def isDataJson(fileName: str) -> bool:
  return fileName == 'data.json'

def walkBillDirs(rootDir = constants.PATH_TO_CONGRESSDATA_DIR, processFile = logName, dirMatch = getTopBillLevel, fileMatch = isDataJson):
    for dirName, subdirList, fileList in os.walk(rootDir):
      if dirMatch(dirName):
        logger.info('Entering directory: %s' % dirName)
        filteredFileList = [fitem for fitem in fileList if fileMatch(fitem)]
        for fname in filteredFileList:
            processFile(dirName=dirName, fileName=fname)

# Utilities. These should go in a utils.py module
def billIdToBillNumber(bill_id: str) -> str:
    """
    Converts a bill_id of the form `hr299-116` into `116hr299`

    Args:
        bill_id (str): hyphenated bill_id from bill status JSON

    Returns:
        str: billCongressTypeNumber (e.g. 116hr299) 
    """
    if not re.match(constants.BILL_ID_REGEX, bill_id):
      raise Exception('bill_id does not have the expected form (e.g. "hjres200-116"')
    return ''.join(reversed(bill_id.split('-')))

def deep_get(dictionary: Dict, *keys):
  """
  A Dict utility to get a field; returns None if the field does not exist

  Args:
      dictionary (Dict): an arbitrary dictionary 

  Returns:
      any: value of the specified key, or None if the field does not exist
  """

  return reduce(
    lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, 
    dictionary)

def loadJSON(filePath: str):
  with open(filePath, 'rb') as f:
    fileDict = json.load(f)
  return fileDict

def getBillCongressTypeNumber(fileDict: Dict):
  bill_id = fileDict.get('bill_id')
  if bill_id:
    return billIdToBillNumber(bill_id)
  else:
    raise Exception('No bill_id: ' + str(fileDict.get('bill_type')))

def getCosponsors(fileDict: Dict, includeFields = []) -> list:
  """
  Gets Cosponsors from data.json Dict. `includeFields` is a list of keys to keep. The most useful are probably 'name' and 'bioguide_id'.

  Args:
      fileDict (Dict): the Dict created from data.json 
      includeFields (list): the fields in the cosponsor object to keep. If no 'includeFields' list is provided, all fields are preserved. 

  Returns:
      list: a list of cosponsors, with selected fields determined by includeFields 
  """
  cosponsors = fileDict.get('cosponsors', [])

  if includeFields:
    cosponsors = list(map(lambda cosponsor: { field: cosponsor.get(field) for field in includeFields }, cosponsors))
  
  # for sponsor in cosponsors:
  #   if not sponsor.get('bioguide_id'):
  #     continue
  #   Sponsor.objects.create(**sponsor)
  return cosponsors

def getBillTitles(fileDict: Dict, include_partial = True, billType = 'all') -> list:
  """
  Get a list of bill titles. If include_partial = True (default), gets all titles. Otherwise, gets only titles that correspond to the whole bill. 

  Args:
      fileDict (Dict): the Dict created from data.json 
      include_partial (bool, optional): Include titles for part of the bill. Defaults to True.
      billType (str, optional): Filter by billType (e.g. 'ih', 'rh', etc.) Defaults to 'all', which does not filter.

  Returns:
      list: a list of titles for the bill; either all titles or only whole-bill titles 
  """
  titles = fileDict.get('titles', [])
  if not include_partial:
    titles = [title for title in titles if not title.get('is_for_portion')]
  
  if (billType != 'all') and constants.BILL_TYPES.get(billType):
    titles = [title for title in titles if constants.BILL_TYPES.get(billType) == title.get('as')]
  return titles

def testWalkDirs():
  filePathList = []
  def addToFilePathList(dirName: str, fileName: str):
    filePathList.append(os.path.join(dirName, fileName))
    print('fpl: ' + str(filePathList))
  walkBillDirs(processFile=addToFilePathList)
  return filePathList

def loadDataJSON(billNumber: str, congressDataDir = constants.PATH_TO_CONGRESSDATA_DIR):
  billNumberMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billNumber)
  [congress, billType, numberOfBill, billVersion, billTypeNumber] = ["" for x in range(5)]
  if billNumberMatch and billNumberMatch.groups():
    [congress, billType, numberOfBill, billVersion] = billNumberMatch.groups()
    billTypeNumber = billType + numberOfBill
  else:
    logger.warning('Bill number is not of the correct form (e.g. 116hr200): {0}'.format(billNumber))
    return

  dataJSONPath = os.path.join(congressDataDir, congress, 'bills', billType, billTypeNumber, 'data.json') 
  if os.path.isfile(dataJSONPath):
    return loadJSON(dataJSONPath)
  else:
    logger.warning('No data.json found for: {0} at {1}'.format(billNumber, dataJSONPath)) 
    return

def loadBillsMeta(billMetaPath = constants.PATH_TO_BILLS_META, zip = True):
  billsMeta = {}
  if zip:
    try:
      with gzip.open(billMetaPath + '.gz', 'rt', encoding='utf-8') as zipfile:
        billsMeta = json.load(zipfile)
    except:
      raise Exception('No file at {0}.gz'.format(billMetaPath))
  else:
    try:
      with open(billMetaPath, 'r') as f:
        billsMeta = json.load(f)
    except:
      raise Exception('No file at {0}.gz'.format(billMetaPath))
  
  return billsMeta

def saveBillsMeta(billsMeta: Dict, metaPath = constants.PATH_TO_BILLS_META, zip = False):
  with open(metaPath, 'w') as f:
    json.dump(billsMeta, f)
    if zip:
      with gzip.open(metaPath + '.gz', 'wt', encoding="utf-8") as zipfile:
        json.dump(billsMeta, zipfile)

def saveBillsMetaToDb():
  billsMeta = loadBillsMeta(billMetaPath = constants.PATH_TO_BILLS_META_GO, zip = False)
  for billnumber, billdata in billsMeta.items():
    billCongressTypeNumber = billdata.get('bill_congress_type_number','') 
    if not billCongressTypeNumber:
      continue
    billNumberMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billCongressTypeNumber)
    [congress, billType, numberOfBill, billVersion, billTypeNumber] = ["" for x in range(5)]
    if billNumberMatch and billNumberMatch.groups():
      [congress, billType, numberOfBill, billVersion] = billNumberMatch.groups()
    else:
      continue
    print('Loading: ' + billCongressTypeNumber)
    metadata = {
      'type': billType,
      'congress': int(congress),
      'number': numberOfBill, 
    }

    for key, value in metadata.items():
      if value:
        billdata[key] = value 
    
    billdata['cosponsors_dict'] = billdata.get('cosponsors', [])
    billdata['committees_dict'] = billdata.get('committees', [])
    keys = billdata.keys()
    if 'cosponsors' in keys:
      del billdata['cosponsors']
    if 'committees' in keys:
      del billdata['committees']
    
    # Avoid not null constraint
    if not billdata.get('related_bills'):
      billdata['related_bills'] = []

    if not billdata.get('cosponsors_dict'):
      billdata['cosponsors_dict'] = []

    if not billdata.get('committees_dict'):
      billdata['committees_dict'] = []

    Bill.objects.update_or_create(bill_congress_type_number=billnumber, defaults=billdata)

def updateBillsMeta(billsMeta= {}):
  def addToBillsMeta(dirName: str, fileName: str):
    billDict = loadJSON(os.path.join(dirName, fileName))
    try:
      billCongressTypeNumber = getBillCongressTypeNumber(billDict)
      logger.debug('billCongressTypeNumber: ' + billCongressTypeNumber)
      if not billCongressTypeNumber:
        logger.warning('!!!!! NO BILL NUMBER !!!!!!')
        return 
    except Exception as err:
      logger.error(err)
      return
    if not billsMeta.get(billCongressTypeNumber):
      billsMeta[billCongressTypeNumber] = {}
    titles = getBillTitles(billDict)
    billsMeta[billCongressTypeNumber]['titles'] = [title.get('title') for title in titles]
    billsMeta[billCongressTypeNumber]['titles_whole_bill'] = [title.get('title') for title in titles if not title.get('is_for_portion')]
    cosponsors = getCosponsors(fileDict=billDict, includeFields=['name', 'bioguide_id'])
    committees = billDict.get('committees', [])
    billsMeta[billCongressTypeNumber]['cosponsors'] = cosponsors
    billsMeta[billCongressTypeNumber]['committees'] = committees

    # TODO convert bill_id to billnumber
    billsMeta[billCongressTypeNumber]['related_bills'] = billDict.get('related_bills')
    for item in billsMeta[billCongressTypeNumber]['related_bills']:
      bill_id = item.get('bill_id') 
      if bill_id:
        item['billCongressTypeNumber'] = billIdToBillNumber(bill_id)
      else:
        item['billCongressTypeNumber'] = None
    billCount = len(billsMeta.keys()) 
    
    utils.dumpRelatedBillJSON(billCongressTypeNumber, billsMeta[billCongressTypeNumber])
    if billCount % constants.SAVE_ON_COUNT == 0:
      saveBillsMeta(billsMeta)

    # Create Bill object
    # bill_data = {
    #   'title': [title.get('title') for title in titles],
    #   'titles_whole_bill': [title.get('title') for title in titles if not title.get('is_for_portion')],
    #   'bill_congress_type_number': billCongressTypeNumber,
    # }
    # bill, created = Bill.objects.get_or_create(
    #   bill_congress_type_number=billCongressTypeNumber,
    #   defaults=bill_data
    # )

    # sponsor_ids = [sponsor['bioguide_id'] for sponsor in cosponsors if sponsor.get('bioguide_id')]
    # qs_sponsor = Sponsor.objects.filter(bioguide_id__in=sponsor_ids)
    # bill.cosponsors.add(*qs_sponsor)

  walkBillDirs(processFile=addToBillsMeta)
  #walkBillDirs(processFile=logName)
  saveBillsMeta(billsMeta)
  return billsMeta

def updateBillsList(bills=[]):
  def addToBillsList(dirName: str, fileName: str):
    billCongressTypeNumber = getBillFromDirname(dirName)
    if billCongressTypeNumber:
      bills.append(billCongressTypeNumber)
  walkBillDirs(processFile=addToBillsList)
  with open(constants.PATH_TO_BILLS_LIST, 'w') as f:
    json.dump(bills, f)
  return bills
