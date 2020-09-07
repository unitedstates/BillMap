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
from billdata import deep_get, billIdToBillNumber, loadJSON, loadDataJSON, saveBillsMeta, loadBillsMeta

PATH_TO_TITLES_INDEX = '../titlesIndex.json'
PATH_TO_RELATEDBILLS = '../relatedBills.json'

OF_YEAR_REGEX = re.compile(r'\sof\s[0-9]+$')

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
        if not billsRelated.get(bill_outer):
            billsRelated[bill_outer] = {'related': {}} 
        
        if not deep_get(billsRelated, bill_outer, 'related'):
            billsRelated[bill_outer]['related'] ={}

        titles = billsMeta[bill_outer].get('titles')
        for title in titles:
            noYearTitle = OF_YEAR_REGEX.sub('', title) 
            similarTitles = filter(lambda titleItem: title != titleItem and titleItem.startswith(noYearTitle), allTitles)
            for similarTitle in similarTitles:
                similarTitleBills = titlesIndex.get(similarTitle)
                for bill_inner in similarTitleBills:
                    # Find a matching item, if any, in the list billsRelated[bill_outer]
                    if not deep_get(billsRelated, bill_outer, 'related', bill_inner):
                        billsRelated[bill_outer]['related'][bill_inner] = {
                            'titles_year': [similarTitle]
                        }
                    elif not deep_get(billsRelated, bill_outer, 'related', bill_inner, 'titles_year'):
                        billsRelated[bill_outer]['related'][bill_inner]['titles_year'] = [similarTitle]
                    else:
                        if similarTitle not in billsRelated[bill_outer]['related'][bill_inner]['titles_year']:
                            billsRelated[bill_outer]['related'][bill_inner]['titles_year'].append(similarTitle)
                    if deep_get(billsRelated, bill_outer, 'related', bill_inner, 'titles_year'):
                        print(billsRelated[bill_outer]['related'][bill_inner])
    return billsRelated 


def addSameTitles(titlesIndex: dict, billsRelated = {}):
    for title, bills in titlesIndex.items():
        for bill_outer in bills:

            # Initialize the key-value for the bill
            if not billsRelated.get(bill_outer):
                billsRelated[bill_outer] = {'related': {}}
            
            if not deep_get(billsRelated, bill_outer, 'related'):
                billsRelated[bill_outer]['related'] = {}

            for bill_inner in bills:
                # Find a matching item, if any, in the list billsRelated[bill_outer]
                if not deep_get(billsRelated, bill_outer, 'related', bill_inner):
                    billsRelated[bill_outer]['related'][bill_inner] = {'titles': [title]}
                else:
                    billsRelated[bill_outer]['related'][bill_inner]['titles'].append(title)

    return billsRelated 

def addGPORelatedBills(billsRelated = {}):
    billsMeta = loadBillsMeta()
    allBills = list(billsMeta.keys())
    if len(billsRelated) == 0:
        try:
            billsRelated = loadJSON(PATH_TO_RELATEDBILLS)
        except Exception:
            pass
    for bill_outer in allBills:

        # Initialize the key-value for the bill
        if not billsRelated.get(bill_outer):
            billsRelated[bill_outer] = {'related': {}}
        
        if not deep_get(billsRelated, bill_outer, 'related'):
            billsRelated[bill_outer]['related'] = {}
        
        billData = loadDataJSON(bill_outer)
        if not billData or not deep_get(billData, 'related_bills'):
            continue

        relatedBillItems = deep_get(billData, 'related_bills')

        for billItem in relatedBillItems:
            billNumber = billIdToBillNumber(billItem.get('bill_id'))
            newDict = {'reason': billItem.get('reason'), 'identified_by': billItem.get('identified_by')}
            print(newDict)
            # Find a matching item, if any, in the list billsRelated[bill_outer]
            if not deep_get(billsRelated, bill_outer, 'related', billNumber):
                billsRelated[bill_outer]['related'][billNumber] =  newDict
            else:
                billsRelated[bill_outer]['related'][billNumber].update(newDict)

    return billsRelated 

def makeAndSaveRelatedBills(titlesIndex = loadTitlesIndex(), relatedBills = loadJSON(PATH_TO_RELATEDBILLS)):
    if not relatedBills:
        sameTitleBills = addSameTitles(titlesIndex)
        relatedBills = addSimilarTitles(titlesIndex=titlesIndex, billsRelated=sameTitleBills)
    relatedBills = addGPORelatedBills(billsRelated=relatedBills)
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

