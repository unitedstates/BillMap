#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, argparse, logging
import re
from typing import Dict

logging.basicConfig(filename='billdata.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def logName(fname: str):
    logger.info('Processing: \t%s' % fname)

def getTopBillLevel(dirName: str):
  return re.match(r'[a-z]+[0-9]+', dirName.split('/')[-1])

def getDataJson(fileName: str):
  return fileName == 'data.json'

def walkBillDirs(rootDir = '../congress', processFile = logName, dirMatch = getTopBillLevel, fileMatch = getDataJson):
    for dirName, subdirList, fileList in os.walk(rootDir):
      if dirMatch(dirName):
        logger.info('Entering directory: %s' % dirName)
        filteredFileList = [fitem for fitem in fileList if fileMatch(fitem)]
        for fname in filteredFileList:
            processFile(fname)

def getBillTitles(congress = '116') -> Dict:
    """
    Creates a dict with key = billnumber, value = [titles]
    """

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.info("You passed an argument.")
  logging.debug("Your Argument: %s" % args.argument)
  
  # TODO pass function to `processFile` to get bill titles
  walkBillDirs()
 
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Generates billdata.json metadata file",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
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