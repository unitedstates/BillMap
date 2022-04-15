#!/usr/bin/env python3
import datetime
import gzip
import json
import logging
import os
import re
import sys

from pytz import timezone
from common import constants

logging.basicConfig(filename='utils.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def getText(item) -> str:
    if item is None:
        return ''

    try:
        if isinstance(item, list):
            item = item[0]
        return item.text
    except:
        return ''


def set_eastern_timezone(obj):
    if isinstance(obj, datetime.datetime):
        return timezone('US/Eastern').localize(obj)
    if isinstance(obj, datetime.date):
        return timezone('US/Eastern').localize(datetime.datetime(obj.year, obj.month, obj.day))
    elif isinstance(obj, str):
        return timezone('US/Eastern').localize(obj.strftime("%Y-%m-%d"))

    try:
        return timezone('US/Eastern').localize(str(obj).strftime("%Y-%m-%d"))
    except:
        return None


def getBillNumberFromBillPath(bill_path: str) -> str:
    """
    Gets billnumber + version from the bill path
    Args:
        bill_path (str): bill path of the form [path]/116/dtd/BILLS-116hr1500rh.xml

    Returns:
        str: e.g. 116hr1500rh
    """

    billnumber_version = re.sub(r'.*\/', '', bill_path).replace('BILLS-', '').replace('.xml', '')
    if constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber_version):
        return billnumber_version
    else:
        return ''


def getBillNumberFromCongressScraperBillPath(bill_path: str) -> str:
    """
    Gets billnumber + version from the bill path
    Args:
        bill_path (str): bill path of the form e.g. [path]/data/116/bills/hr/hr1/text-versions

    Returns:
        str: e.g. 116hr1500rh
    """

    match = constants.US_CONGRESS_PATH_REGEX_COMPILED.search(bill_path)
    billnumber_version = ''
    if match:
        match_groups = match.groupdict()
        version = match_groups.get('version', '')
        if version is None:
            version = ''
        billnumber_version = match_groups.get('congress', '') + match_groups.get('billnumber', '') + version
    else:
        raise Exception('No match for bill number in bill path')
    return billnumber_version


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
    relatedBillJSONPath = os.path.join(relatedBillDirPath, billCongressTypeNumber + '.json')
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


def dumpRelatedBillJSON(
        billCongressTypeNumber, relatedBillJSON,
        relatedBillDirPath=constants.PATH_TO_RELATEDBILLS_DIR
):
    if not os.path.isdir(relatedBillDirPath):
        os.mkdir(relatedBillDirPath)
    relatedBillJSONPath = os.path.join(relatedBillDirPath, billCongressTypeNumber + '.json')
    if not relatedBillJSON:
        relatedBillJSON = {'related': {}}
    with open(relatedBillJSONPath, 'w') as f:
        try:
            json.dump(relatedBillJSON, f)
            logger.debug('Saved to: ' + relatedBillJSONPath)
        except Exception as err:
            raise Exception('Error storing ' + relatedBillJSONPath + ': ' + str(err))
