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

# NOTE: This is very slow. Takes ~20 minutes
def addSimilarTitles(titlesIndex: dict, billsRelated = {}):
    allTitles = list(titlesIndex.keys())
    billsMeta = loadBillsMeta()
    allBills = list(billsMeta.keys())
    for bill_outer in allBills:
        relatedBillItem = billsRelated.get(bill_outer)
            
        # Initialize the key-value for the bill
        if not relatedBillItem:
            billsRelated[bill_outer] = []

        titles = billsMeta[bill_outer].get('titles')
        for title in titles:
            noYearTitle = re.sub(r'\sof\s[0-9]+$', '', title) 
            similarTitles = filter(lambda titleItem: titleItem.startswith(noYearTitle) and title != titleItem, allTitles)
            for similarTitle in similarTitles:
                similarTitleBills = titlesIndex.get(similarTitle)
                for bill_inner in similarTitleBills:
                    # Find a matching item, if any, in the list billsRelated[bill_outer]
                    # See https://stackoverflow.com/a/1701404/628748
                    bill_index = next((i for i,v in enumerate(billsRelated.get(bill_outer)) if (bill_inner == v.get('billCongressTypeNumber'))), None)
                    if not bill_index:
                        billsRelated[bill_outer].append({
                            'billCongressTypeNumber': bill_inner,
                            'titles_year': [similarTitle]
                        })
                    elif not billsRelated[bill_outer][bill_index].get('titles_year'):
                        billsRelated[bill_outer][bill_index]['titles_year'] = [similarTitle]
                    else:
                        if similarTitle not in billsRelated[bill_outer][bill_index]['titles_year']:
                            billsRelated[bill_outer][bill_index]['titles_year'].append(similarTitle)
                    # if bill_index and billsRelated[bill_outer][bill_index].get('titles_year'):
                    #    print(billsRelated[bill_outer][bill_index])
    return billsRelated 


def addSameTitles(titlesIndex: dict, billsRelated = {}):
    for title, bills in titlesIndex.items():
        for bill_outer in bills:
            relatedBillItem = billsRelated.get(bill_outer)
            
            # Initialize the key-value for the bill
            if not relatedBillItem:
                billsRelated[bill_outer] = []

            for bill_inner in bills:
                # Find a matching item, if any, in the list billsRelatedByTitle[bill_outer]
                # See https://stackoverflow.com/a/1701404/628748
                bill_index = next((i for i,v in enumerate(billsRelated[bill_outer]) if (bill_inner == v.get('billCongressTypeNumber'))), None)
                if not bill_index:
                    billsRelated[bill_outer].append({
                        'billCongressTypeNumber': bill_inner,
                        'titles': [title]
                    })
                else:
                    billsRelated[bill_outer][bill_index]['titles'].append(title)

    return billsRelated 

def getRelatedBills(titlesIndex = loadTitlesIndex()):
    billsRelatedIndex = addSameTitles(titlesIndex)
    return billsRelatedIndex

def makeAndSaveRelatedBills(titlesIndex = loadTitlesIndex()):
    sameTitleBills = getRelatedBills(titlesIndex)
    relatedBills = addSimilarTitles(titlesIndex=titlesIndex, billsRelated=sameTitleBills)
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

