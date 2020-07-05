#!/usr/bin/env python3
#
# Command line template from https://gist.githubusercontent.com/opie4624/3896526/raw/3aff2ad7030a74ce26f9fcf80791ae0396d84f18/commandline.py

import sys, os, argparse, logging
from typing import Dict

logging.basicConfig(filename='billdata.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def logName(fname: str):
    logger.info('Processing: \t%s' % fname)

def walkBillDirs(rootDir = '.', processFile = logName):
    for dirName, subdirList, fileList in os.walk(rootDir):
        logger.info('Entering directory: %s' % dirName)
        for fname in fileList:
            processFile(fname)

def getBillTitles(congress = '116') -> Dict:
    """
    Creates a dict with key = billnumber, value = [titles]
    """

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.info("You passed an argument.")
  logging.debug("Your Argument: %s" % args.argument)
 
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
  # TODO Specify your real parameters here.
  parser.add_argument(
                      "argument",
                      help = "pass ARG to the program",
                      metavar = "ARG")
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO
  
  main(args, loglevel)