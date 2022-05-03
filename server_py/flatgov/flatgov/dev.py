from .settings import *

DEBUG = True

INSTALLED_APPS += [
    'common',
    'fetch_bill',
]


DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'flatgov',
       'USER': 'vmm',
       'PASSWORD': 'vmm',
       'HOST': 'localhost',
       'PORT': 5432,
    },
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


CONGRESS_DATA_PATH = os.path.join(BASE_DIR, 'congress', 'data')
BILLS_JSON_PATH = os.path.join(BASE_DIR, 'json_data') 
RELATED_BILLS_JSON_PATH = os.path.join(BILLS_JSON_PATH, 'relatedBills.json') 
BILLS_META_JSON_PATH = os.path.join(BILLS_JSON_PATH, 'billsMeta.json') 
TITLES_INDEX_JSON_PATH = os.path.join(BILLS_JSON_PATH, 'titlesIndex.json')


PATH_SEC_602 = os.path.join(BASE_DIR, 'samples/116hr5150-sec602.txt')
PATH_MAL = os.path.join(BASE_DIR, 'samples/maralago.txt')
PATH_BILLSECTIONS_JSON = os.path.join(
    BASE_DIR, 'elasticsearch/billsections_mapping.json')
PATH_BILL_FULL_JSON = os.path.join(
    BASE_DIR, 'elasticsearch/bill_full_mapping.json')


PATH_TO_BILLS_META = os.path.join(BASE_DIR, 'billsMeta.json')
PATH_TO_BILLS_META_GO = os.path.join(BASE_DIR, 'billMetaGo.json')
BILLMETA_GO_CMD = 'billmeta'
ESQUERY_GO_CMD = 'esquery'
COMPAREMATRIX_GO_CMD = 'comparematrix'
PATH_TO_CONGRESSDATA_DIR = CONGRESS_DATA_PATH
PATH_TO_DATA_DIR = os.getenv('PATH_TO_DATA_DIR', os.path.join('/', *"/usr/local/share/xcential/public/data".split('/')))
PATH_TO_CONGRESSDATA_XML_DIR = os.getenv('PATH_TO_CONGRESSDATA_XML_DIR', os.path.join('/', *"/usr/local/share/xcential/public/data/116/dtd".split('/')))
PATH_TO_BILLS_LIST = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'billList.json')
PATH_TO_TITLES_INDEX = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'titlesIndex.json')
PATH_TO_NOYEAR_TITLES_INDEX = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'noYearTitlesIndex.json')
PATH_TO_RELATEDBILLS_DIR = os.path.join(PATH_TO_CONGRESSDATA_DIR, 'relatedbills')

USCONGRESS_XML_FILE = 'data.xml'

ALLOWED_HOSTS = ['127.0.0.1']
