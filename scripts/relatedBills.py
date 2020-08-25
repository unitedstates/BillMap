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
    newIndex = {}
    for key, value in titlesIndex.items():
        for bill in value:
            if newIndex.get(bill):
                if not newIndex[bill]:
                    newIndex[bill].append(bill)
            else:
                newIndex[bill] = [bill]
    return newIndex


def makeAndSaveSameTitleIndex():
    sameTitlesIndex = getSameTitles()
    saveBillsMeta(billsMeta=sameTitlesIndex,
                  metaPath=PATH_TO_SAME_TITLES_INDEX)


def main():
    makeAndSaveSameTitleIndex()


main()
