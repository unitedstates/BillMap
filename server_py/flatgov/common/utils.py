
#!/usr/bin/env python3
import sys, os
import logging
import gzip
import json
from common import constants

logging.basicConfig(filename='utils.log',
                    filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def loadTitlesIndex(titleIndexPath=constants.PATH_TO_TITLES_INDEX, zip=True):
    titlesIndex = {}
    if zip:
        try:
            with gzip.open(titleIndexPath + '.gz', 'rt', encoding='utf-8') as zipfile:
                titlesIndex = json.load(zipfile)
        except:
            raise Exception('No file at' + titleIndexPath + '.gz')
    else:
        try:
            with open(titleIndexPath, 'r') as f:
                titlesIndex = json.load(f)
        except:
            raise Exception('No file at' + titleIndexPath + '.gz')

    return titlesIndex

def loadRelatedBillJSON(billCongressTypeNumber, relatedBillDirPath=constants.PATH_TO_RELATEDBILLS_DIR):
    relatedBillJSONPath = os.path.join(relatedBillDirPath, billCongressTypeNumber +'.json')
    relatedBillJSON = {'related': {}}
    if os.path.isfile(relatedBillJSONPath):
        with open(relatedBillJSONPath, 'r') as f:
            try:
                relatedBillJSON = json.load(f)
            except Exception as err:
                raise Exception('Error loading ' + relatedBillJSONPath + ': ' + str(err))
    else:
        with open(relatedBillJSONPath, 'w') as f:
            json.dump(relatedBillJSON, f)

    return relatedBillJSON 

def dumpRelatedBillJSON(billCongressTypeNumber, relatedBillJSON, relatedBillDirPath=constants.PATH_TO_RELATEDBILLS_DIR):
    relatedBillJSONPath = os.path.join(relatedBillDirPath, billCongressTypeNumber +'.json')
    if not relatedBillJSON:
        relatedBillJSON = {'related': {}}
    with open(relatedBillJSONPath, 'w') as f:
        try:
            json.dump(relatedBillJSON, f)
            logger.debug('Saved to: ' + relatedBillJSONPath)
        except Exception as err:
            raise Exception('Error storing ' + relatedBillJSONPath + ': ' + str(err))