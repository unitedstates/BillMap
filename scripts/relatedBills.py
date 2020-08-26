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


def getRelatedBills():
    billsMeta = loadBillsMeta()
    titlesIndex = loadTitlesIndex()
    billsRelatedIndex = {key: [] for key in billsMeta.keys()}
    getSameTitles(titlesIndex, billsRelatedIndex)
    return billsRelatedIndex
    # for key, value in billsRelatedIndex.items():
    #     if len(value) > 1:
    #         print(key, value)


def getSameTitles(titlesIndex, billsRelatedIndex):
    for title, bills in titlesIndex.items():
        for billNum in bills:
            similarList = billsRelatedIndex.get(billNum)
            if len(similarList) == 0:
                for bill in bills:
                    similarList.append({
                        'billCongressTypeNumber': bill,
                        'titles': [title]
                    })
            else:
                for item in similarList:
                    item.get('titles').append(title)


# def makeAndSaveSameTitleIndex():
#     sameTitlesIndex = getSameTitles()
#     saveBillsMeta(billsMeta=sameTitlesIndex,
#                   metaPath=PATH_TO_SAME_TITLES_INDEX)
# def main():
#     makeAndSaveSameTitleIndex()
# main()
getRelatedBills()
