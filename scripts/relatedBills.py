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
from billdata import saveBillsMeta

PATH_TO_TITLES_INDEX = '../titlesIndex.json'
PATH_TO_SAME_TITLES_INDEX = '../sameTitles.json'

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


def getSameTitles():
    titlesIndex = loadTitlesIndex()
    sameTitlesIndex = {}
    for title, bills in titlesIndex.items():
        for bill in bills:
            if not sameTitlesIndex.get(bill):
                sameTitlesIndex[bill] = {
                    'same_titles': bills
                }
            else:
                current_same_titles = sameTitlesIndex[bill].get('same_titles')
                if current_same_titles:
                    combined_bills = list(set(current_same_titles + bills))
                    sameTitlesIndex[bill]['same_titles'] = combined_bills

    return sameTitlesIndex


def makeAndSaveSameTitleIndex():
    sameTitlesIndex = getSameTitles()
    saveBillsMeta(billsMeta=sameTitlesIndex,
                  metaPath=PATH_TO_SAME_TITLES_INDEX)


def main():
    makeAndSaveSameTitleIndex()


main()
