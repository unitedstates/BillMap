from logging import currentframe
import sys
import os
import argparse
import logging
import re
import json
import gzip
import datetime
from typing import Dict
from functools import reduce
from billdata import saveBillsMeta, loadJSON, loadBillsMeta

PATH_TO_TITLES_INDEX = '../titlesIndex.json'
PATH_TO_RELATEDBILLS = '../relatedBills.json'

logging.basicConfig(filename='billdata.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def loadTitlesIndex(titleIndexPath=PATH_TO_TITLES_INDEX, zip=True):
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

def getSimilarTitles(titlesIndex: dict, same=True):
    billsRelatedByTitle = {}
    for title, bills in titlesIndex.items():
        for bill_outer in bills:
            similarTitles = billsRelatedByTitle.get(bill_outer)
            
            # Initialize the key-value for the bill
            if not similarTitles:
                billsRelatedByTitle[bill_outer] = []

            for bill_inner in bills:
                # Find a matching item, if any, in the list billsRelatedByTitle[bill_outer]
                # See https://stackoverflow.com/a/1701404/628748
                bill_index = next((i for i,v in enumerate(billsRelatedByTitle[bill_outer]) if (bill_inner == v.get('billCongressTypeNumber'))), None)
                if not bill_index:
                    billsRelatedByTitle[bill_outer].append({
                        'billCongressTypeNumber': bill_inner,
                        'titles': [title]
                    })
                else:
                    billsRelatedByTitle[bill_outer][bill_index]['titles'].append(title)

    return billsRelatedByTitle 

def getRelatedBills():
    billsMeta = loadBillsMeta()
    titlesIndex = loadTitlesIndex()
    billsRelatedIndex = getSimilarTitles(titlesIndex)
    return billsRelatedIndex

def makeAndSaveRelatedBills():
    relatedBills = getRelatedBills()
    saveBillsMeta(billsMeta=relatedBills,
                   metaPath=PATH_TO_RELATEDBILLS)

def main(args, loglevel):
    makeAndSaveRelatedBills()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generates relatedbills.json metadata file",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
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

