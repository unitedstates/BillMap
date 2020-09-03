import datetime

PATH_TO_BILLS_META = '../billsMeta.json'
SAVE_ON_COUNT = 1000

BILL_TYPES = {
  'ih': 'introduced',
  'rh': 'reported to house'
}

CURRENT_CONGRESSIONAL_YEAR = datetime.date.today().year if datetime.date.today() > datetime.date(datetime.date.today().year, 1, 3) else (datetime.date.today().year - 1)
CURRENT_CONGRESS, cs_temp = divmod(round(((datetime.date(CURRENT_CONGRESSIONAL_YEAR, 1, 3) - datetime.date(1788, 1, 3)).days) / 365) + 1, 2)
CURRENT_SESSION = cs_temp + 1