
#!/usr/bin/env python3

import sys, logging, argparse
from billdata import loadBillsMeta, saveBillsMeta

logging.basicConfig(filename='process_bill_meta.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
PATH_TO_TITLES_INDEX = '../titlesIndex.json'

def makeTitleIndex():
    billsMeta = loadBillsMeta()
    titlesIndex = {}
    for key, value in billsMeta.items():
        titles = list(set(value.get('titles')))
        for title in titles:
            if titlesIndex.get(title):
                titlesIndex[title].append(key)
            else:
                titlesIndex[title] = [key] 
    return titlesIndex

def makeAndSaveTitlesIndex():
    titlesIndex = makeTitleIndex()
    saveBillsMeta(billsMeta = titlesIndex, metaPath = PATH_TO_TITLES_INDEX)

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.info("You passed an argument.")
  logging.debug("Your Argument: %s" % args.argument)
  
  makeAndSaveTitlesIndex()
  # makeAndSaveSimilarityMeta
 
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