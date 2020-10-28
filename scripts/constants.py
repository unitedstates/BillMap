import os
import re
import datetime
import os
from copy import deepcopy
from re import S

PATH_TO_BILLS_META = os.path.join('..', 'billsMeta.json')
PATH_TO_CONGRESSDATA_DIR = os.path.join('..', '..', 'congress', 'data')
PATH_TO_DATA_DIR = os.path.join('/', *"/usr/local/share/xcential/public/data".split('/'))
PATH_TO_CONGRESSDATA_XML_DIR = os.path.join('/', *"/usr/local/share/xcential/public/data/116/dtd".split('/'))
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

SAMPLE_QUERY = {
  "query": {
    "match": {
      "headers": {
        "query": "date"
      }
    }
  }
}

SAMPLE_QUERY_W_CONGRESS = {
  "query": {
    "bool": {
      "must": [
         { "match": {
              "headers": {
              "query": "date"
              }
         }
        }
      ],
      "filter": [{
        "term": {
          "congress": "115"
        }
      }]
    }
  }
}

SAMPLE_QUERY_NESTED = {
  "query": {
    "nested": {
      "path": "sections",
      "query": {
        "bool": {
          "must": [
            { "match": { "sections.section_header": "title" }}
          ]
        }
      },
      "inner_hits": { 
        "highlight": {
          "fields": {
            "sections.section_header": {}
          }
        }
      }
    }
  }
}

# more like this query (working)
SAMPLE_QUERY_MLT_HEADERS  = {"query": {
  "more_like_this": {
    "fields": ["headers"],
    "like": "Dependent care credit improvements",
    "min_term_freq" : 1,
    "max_query_terms" : 10,
    "min_doc_freq" : 1 
  }
}
}

reporting_requirement = """
Not later than 5 years after the date of enactment of this Act, the administering Secretaries, acting jointly, shall report to the appropriate committees of Congress on the progress in the reduction of food waste that can be attributed to the standardization of food date labeling and consumer education required by this Act and the amendments made by this Act
"""

quality_date_guidance = """
The Commissioner of Food and Drugs and the Secretary of Agriculture shall establish guidance for food labelers on how to determine quality dates and safety dates for food products.
"""

def getQueryText(text_path: str = '../samples/maralago.txt'):
  with open(text_path, 'r') as f:
    return f.read()

# more like this query (working)
SAMPLE_QUERY_NESTED_MLT = {
  "query": {
    "nested": {
      "path": "sections",
      "query": {
        "more_like_this": {
          "fields": ["sections.section_text"],
          "like": reporting_requirement,
          "min_term_freq" : 2,
          "max_query_terms" : 10,
          "min_doc_freq" : 3 
        }
      },
      "inner_hits": {
          "highlight": {
          "fields": {
            "sections.section_text": {}
          }
        }
      }
    }
  }
}

SAMPLE_QUERY_NESTED_MLT_MARALAGO =  deepcopy(SAMPLE_QUERY_NESTED_MLT)
SAMPLE_QUERY_NESTED_MLT_MARALAGO['query']['nested']['query']['more_like_this']['like'] = getQueryText()
SAMPLE_QUERY_NESTED_MLT_116hr5150sec602 = deepcopy(SAMPLE_QUERY_NESTED_MLT)
SAMPLE_QUERY_NESTED_MLT_116hr5150sec602['query']['nested']['query']['more_like_this']['like'] = getQueryText('../samples/116hr5150-sec602.txt')

def makeMLTQuery(queryText: str, queryTextPath: str='../samples/116hr5150-sec602.txt'):
  if queryTextPath and not queryText:
    try:
      queryText = getQueryText(queryTextPath)
    except Exception as err:
      raise Exception('Error getting text from path: {0}'.format(err))

  newQuery = deepcopy(SAMPLE_QUERY_NESTED_MLT)
  newQuery['query']['nested']['query']['more_like_this']['like'] = queryText 
  return newQuery