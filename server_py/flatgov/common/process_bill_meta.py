#!/usr/bin/env python3

import sys
import re
import logging

from common.billdata import loadBillsMeta, saveBillsMeta
from common import constants

logging.basicConfig(filename='process_bill_meta.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def makeTitleIndex():
    billsMeta = loadBillsMeta()
    titlesIndex = {}
    for key, value in billsMeta.items():
        titles = list(dict.fromkeys(value.get('titles')))
        for title in titles:
            if titlesIndex.get(title):
                titlesIndex[title].append(key)
            else:
                titlesIndex[title] = [key]
    return titlesIndex


def makeNoYearTitleIndex():
    billsMeta = loadBillsMeta()
    noYearTitlesIndex = {}
    for key, value in billsMeta.items():
        titles = list(dict.fromkeys(value.get('titles')))
        for title in titles:
            # truncate year from title
            noYearTitle = re.sub(r'of\s[0-9]{4}$', '', title)
            if noYearTitle != title:
                if noYearTitlesIndex.get(noYearTitle):
                    noYearTitlesIndex[noYearTitle].append(key)
                else:
                    noYearTitlesIndex[noYearTitle] = [key]
    return noYearTitlesIndex


def makeAndSaveTitlesIndex():
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    logging.info("You passed an argument.")
    # logging.debug("Your Argument: %s" % args.argument)

    titlesIndex = makeTitleIndex()
    saveBillsMeta(billsMeta=titlesIndex, metaPath=constants.PATH_TO_TITLES_INDEX)
    noYearTitlesIndex = makeNoYearTitleIndex()
    saveBillsMeta(billsMeta=noYearTitlesIndex, metaPath=constants.PATH_TO_NOYEAR_TITLES_INDEX)
