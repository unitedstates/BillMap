import os
import re
import datetime
import os

PATH_TO_BILLS_META = os.path.join('..', 'billsMeta.json')
PATH_TO_CONGRESSDATA_DIR = os.path.join('..', '..', 'congress', 'data')
PATH_TO_BILLS_LIST = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'billList.json')
PATH_TO_TITLES_INDEX = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'titlesIndex.json')
PATH_TO_NOYEAR_TITLES_INDEX = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'noYearTitlesIndex.json')
PATH_TO_RELATEDBILLS_DIR = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'relatedbills')
#PATH_TO_RELATEDBILLS = '../relatedBills.json'
SAVE_ON_COUNT = 1000

BILL_ID_REGEX = r'[a-z]+[1-9][0-9]*-[1-9][0-9]+'
BILL_NUMBER_REGEX = r'([1-9][0-9]*)([a-z]+)([0-9]+)([a-z]+)?$'
BILL_DIR_REGEX = r'.*?([1-9][0-9]*)\/bills\/[a-z]+\/([a-z]+)([0-9]+)$'
BILL_NUMBER_REGEX_COMPILED = re.compile(BILL_NUMBER_REGEX)
BILL_DIR_REGEX_COMPILED = re.compile(BILL_DIR_REGEX)

BILL_TYPES = {
  'ih': 'introduced',
  'rh': 'reported to house'
}

CURRENT_CONGRESSIONAL_YEAR = datetime.date.today().year if datetime.date.today() > datetime.date(datetime.date.today().year, 1, 3) else (datetime.date.today().year - 1)
CURRENT_CONGRESS, cs_temp = divmod(round(((datetime.date(CURRENT_CONGRESSIONAL_YEAR, 1, 3) - datetime.date(1788, 1, 3)).days) / 365) + 1, 2)
CURRENT_SESSION = cs_temp + 1