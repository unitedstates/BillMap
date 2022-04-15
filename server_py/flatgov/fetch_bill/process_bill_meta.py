
#!/usr/bin/env python3

import sys
import re
import logging
import argparse
try:
    from flatgovtools.billdata import loadBillsMeta, saveBillsMeta
    from flatgovtools import constants
except:
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
    titlesIndex = makeTitleIndex()
    saveBillsMeta(billsMeta=titlesIndex, metaPath=constants.PATH_TO_TITLES_INDEX)
    noYearTitlesIndex = makeNoYearTitleIndex()
    saveBillsMeta(billsMeta=noYearTitlesIndex, metaPath=constants.PATH_TO_NOYEAR_TITLES_INDEX)


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    logging.info("You passed an argument.")
    logging.debug("Your Argument: %s" % args.argument)

    makeAndSaveTitlesIndex()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generates billdata.json metadata file",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        "-a",
        "--argument",
        action='store',
        dest='argument',
        help="sample argument"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest='verbose',
        help="increase output verbosity",
        action="store_true"
    )
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        LOGLEVEL = logging.DEBUG
    else:
        LOGLEVEL = logging.INFO

    main(args, LOGLEVEL)
