#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, argparse, logging, re, json, gzip
from typing import Dict
from functools import reduce

try:
  from . import constants
  from . import utils
except:
  import constants
  import utils

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
    return None
  

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
  cosponsors = fileDict.get('cosponsors')

  if includeFields:
    cosponsors = list(map(lambda cosponsor: { field: cosponsor.get(field) for field in includeFields }, cosponsors))

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
  titles = fileDict.get('titles')
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
    logger.warning('Bill number is not of the correct form (e.g. 116hr200): ' + billNumber)
    return

  dataJSONPath = os.path.join(congressDataDir, congress, 'bills', billType, billTypeNumber, 'data.json') 
  if os.path.isfile(dataJSONPath):
    return loadJSON(dataJSONPath)
  else:
    logger.warning('No data.json found for: ' + billNumber + ' at ' + dataJSONPath) 
    return

def loadBillsMeta(billMetaPath = constants.PATH_TO_BILLS_META, zip = True):
  billsMeta = {}
  if zip:
    try:
      with gzip.open(billMetaPath + '.gz', 'rt', encoding='utf-8') as zipfile:
        billsMeta = json.load(zipfile)
    except:
      raise Exception('No file at' + billMetaPath + '.gz')
  else:
    try:
      with open(billMetaPath, 'r') as f:
        billsMeta = json.load(f)
    except:
      raise Exception('No file at' + billMetaPath + '.gz')
  
  return billsMeta

def saveBillsMeta(billsMeta: Dict, metaPath = constants.PATH_TO_BILLS_META, zip = True):
  with open(metaPath, 'w') as f:
    json.dump(billsMeta, f)
    if zip:
      with gzip.open(metaPath + '.gz', 'wt', encoding="utf-8") as zipfile:
        json.dump(billsMeta, zipfile)

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
    billsMeta[billCongressTypeNumber]['cosponsors'] = getCosponsors(fileDict=billDict, includeFields=['name', 'bioguide_id'])

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

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.info("You passed an argument.")
  logging.debug("Your Argument: %s" % args.argument)
  
  # TODO consider loading billsMeta before updating
  # TODO consider updating only current congress
  updateBillsList()
  updateBillsMeta()
 
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Generates billdata.json metadata file",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
  parser.add_argument(
                      "-a",
                      "--argument",
                      action='store',
                      dest='argument',
                      help="sample argument")
  parser.add_argument(
                      "-v",
                      "--verbose",
                      dest='verbose',
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO
  
  main(args, loglevel)