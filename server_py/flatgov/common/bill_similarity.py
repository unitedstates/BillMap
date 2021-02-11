import os
import json
import re
from typing import List
from lxml import etree
from operator import itemgetter
from elasticsearch import exceptions, Elasticsearch
es = Elasticsearch()
from collections import OrderedDict
from iteration_utilities import flatten, unique_everseen, duplicates

from common.utils import getText, getBillNumberFromBillPath, getBillNumberFromCongressScraperBillPath 
from django.conf import settings
from common import constants
from bills.models import Bill

bill_file = "BILLS-116hr1500rh.xml"
bill_file2 = "BILLS-116hr299ih.xml"
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)

BASE_DIR = settings.BASE_DIR

# The max number of bills to get for each section
MAX_BILLS_SECTION = 20

def runQuery(index: str='billsections', query: dict=constants.SAMPLE_QUERY_NESTED_MLT_MARALAGO, size: int=10) -> dict:
  query = query
  # See API documentation
  # https://elasticsearch-py.readthedocs.io/en/v7.10.1/api.html#elasticsearch.Elasticsearch.search
  return es.search(index=index, body=query, size=size)

def getXMLDirByCongress(congress: str ='116', docType: str = 'dtd', uscongress: bool = True) -> str:
  if uscongress:
    return os.path.join(BASE_DIR, 'congress', 'data', congress, 'bills')
  return os.path.join(constants.PATH_TO_DATA_DIR, congress, docType)

def getMapping(map_path):
    with open(map_path, 'r') as f:
        return json.load(f)

def setBillNumberQuery(billnumber: str) -> dict:
  """
  Sets Elasticsearch query by bill number
  Args:
      billnumber (str): billnumber (no version) 

  Returns:
      dict: [description]
      "hits" : [
        {
          "_index" : "billsections",
          "_type" : "_doc",
          "_id" : "yH0adHcByMv3L6kFHKWS",
          "_score" : null,
          "fields" : {
             "date" : [
              "2019-03-05T00:00:00.000Z"
            ],
            "billnumber" : [
              "116hr1500"
            ],
            "id" : [
              "116hr1500ih"
            ],
            "bill_version" : [
              "ih"
            ],
            "dc" : [
             ... 
            ]
          },
          "sort" : [
            1558569600000
          ]
        },
  """
  return {
  "sort" : [
  { "date" : {"order" : "desc"}}
  ],
  "query": {
    "match": {
      "billnumber": billnumber
    }
  },
  "fields": ["id", "billnumber", "billversion", "billnumber_version", "date"],
  "_source": False
}
  
def getBillPath(billnumber: str) -> str:
  """
   Get the path of the form [path to congress/data]/116/hr/hr1500
  Args:
      billnumber (str): [description]

  Returns:
      str: [description]
  """
  bill_path = ''
  billMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber) 
  if billMatch and billMatch.groupdict():
      billMatchGroups = billMatch.groupdict()
      xmlDir = getXMLDirByCongress(congress=billMatchGroups.get('congress'))
      bill_path = os.path.join(xmlDir, billMatchGroups.get('stage'), billMatchGroups.get('stage') + billMatchGroups.get('number'))
  else:
    raise Exception(billnumber + ': billnumber is not of the expected form')
  return bill_path

def getBillStatus(billnumber: str):
  """
  Get billstatus in XML by bill number

  Args:
      billnumber (str): billnumber (without version) 

  Returns:
      etree:  an etree of the fdsys_billstatus.xml
  """
  billMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber) 
  if not billMatch:
    raise Exception(billnumber + ': bill number is not of the expected form')
  billstatus_path = ''
  try:
      billstatus_path = os.path.join(getBillPath(billnumber), 'fdsys_billstatus.xml')
      return etree.parse(billstatus_path)
  except:
    print('Could not parse bill status at: ' + billstatus_path)
    pass
  return None


BILL_VERSIONS = {
  'Referred in Senate': 'rfs',
  'Enrolled Bill': 'enr'
}

def getLatestBillVersion(billnumber: str) -> str:
  """
  Find latest version from Fdsys_billstatus 
    TODO sort by date
    Currently assume that the first item is the oldest
        <item>
        <type>Placed on Calendar Senate</type>
        <date>2019-03-14T04:00:00Z</date>
        <formats>
          <item>
            <url>https://www.govinfo.gov/content/pkg/BILLS-116hr1pcs/xml/BILLS-116hr1pcs.xml</url>
          </item>
        </formats>
      </item>

  Args:
      billnumber (str): billnumber (without version) 

  Returns:
      str: version (e.g. 'ih', 'eh', 'enr', etc.) 
  """
  billStatus = getBillStatus(billnumber)
  try:
    billTypes = billStatus.xpath('//textVersions/item[1]/type')
    if billTypes is not None and billTypes[0] is not None:
      billType = billTypes[0].text
      if billType in ['Enrolled Bill', 'Referred in Senate']:
        billversion = BILL_VERSIONS[billType]
      else:
        billversion = re.sub('[a-z ]', '', billTypes[0].text).lower()
    else:
      raise Exception('No bill type found in bill status for: ' + billnumber)
    billnumber_version = billnumber + billversion
    return billnumber_version
  except Exception as err:
    print(err)
    print('Using search to get the latest version for: ' + billnumber)
    pass
  return getLatestBillVersionSearch(billnumber)

def getLatestBillVersionSearch(billnumber: str) -> str:
  """
  Find latest version in Elasticsearch

  Args:
      billnumber (str): billnumber (without version) 

  Returns:
      str: version (e.g. 'ih', 'eh', 'enr', etc.) 
  """
  bills = runQuery(index='billsections', query=setBillNumberQuery(billnumber))
  billversion = ''
  if bills.get('hits', {}).get('total', {}).get('value', {}) and bills.get('hits', {}).get('total', {}).get('value', {}) > 0:
      tophit = bills.get('hits').get('hits')[0].get('fields')
      billnumber = tophit.get('billnumber')[0] 
      billversion = tophit.get('billversion', '')[0]

  return billnumber + billversion

def getCleanSimilars(similarBills: dict) -> dict: 
  """
  Creates a dict where the key is the index of the original bill section 
  and the value is an array of similar sections from other bills

  Args:
      similarBills (dict): similar bills, with a list of sections that match the original bill 

  Returns:
      dict: similar sections, keyed by the index of the original bill's sections {0: [similar sections], 1: [...], 3: [...] } 
  """
  similarsDict = {} 
  for similarSections in similarBills.values():
    for similarSection in similarSections:
      currentIndex = str(similarSection.get('sectionIndex'))
      if not similarsDict.get(currentIndex):
        similarsDict[currentIndex] = [similarSection]
      else:
        similarsDict[currentIndex].append(similarSection)

  return similarsDict

def processBill(bill_path: str=PATH_BILL):
  try:
    billTree = etree.parse(bill_path)
  except:
    raise Exception('Could not parse bill')
  dublinCores = billTree.xpath('//dublinCore')
  if (dublinCores is not None) and (dublinCores[0] is not None):
    dublinCore = etree.tostring(dublinCores[0], method="xml", encoding="unicode"),
  else:
    dublinCore = ''
  congress = billTree.xpath('//form/congress')
  congress_text = re.sub(r'[a-zA-Z ]+$', '', getText(congress))
  # session = billTree.xpath('//form/session')
  # session_text = re.sub(r'[a-zA-Z ]+$', '', getText(session))
  legisnum = billTree.xpath('//legis-num')
  legisnum_text = getText(legisnum)
  billnumber_version = getBillNumberFromCongressScraperBillPath(bill_path) 
  if billnumber_version == '':
    billnumber_version = getBillNumberFromBillPath(bill_path)
  billnumber = ''
  if billnumber_version:
    billnumber = re.sub(r'[a-z]*$', '', billnumber_version)
  else:
    raise Exception('Could not get billnumber and version')
  sections = billTree.xpath('//section[not(ancestor::section)]')

  #print('Bill number: {0}'.format(billnumber))
  #print('Bill number + version: {0}'.format(billnumber_version))

  qs_bill = Bill.objects.filter(bill_congress_type_number=billnumber)
  if qs_bill.exists():
    bill = qs_bill.first()
    es_similarity = list()

    for section in sections:
      if (section.xpath('header') and len(section.xpath('header')) > 0  and section.xpath('enum') and len(section.xpath('enum'))>0):
        section_item = {
          'billnumber': billnumber,
          'billnumber_version': billnumber_version,
          'section_number': section.xpath('enum')[0].text,
          'section_header':  section.xpath('header')[0].text,
        }
      else:
        section_item = {
          'billnumber': billnumber,
          'billnumber_version': billnumber_version,
          'section_number': '',
          'section_header': '',
        }
      section_text = etree.tostring(section, method="text", encoding="unicode")

      similarity = moreLikeThis(queryText=section_text)
      similar_sections = sorted(getSimilarSections(similarity), key=itemgetter('score'), reverse=True)
      section_item['similars'] = similar_sections
      es_similarity.append(section_item)

    similarBills = getSimilarBills(es_similarity)
    bill.es_similar_bills_dict = similarBills
    cleanedSimilars = getCleanSimilars(similarBills)
    for sectionIndex, sectionItem in enumerate(es_similarity):
      es_similarity[sectionIndex]["similars"] = cleanedSimilars.get(str(sectionIndex), [])

    bill.es_similarity = es_similarity
    try:
      bill.save(update_fields=['es_similarity', 'es_similar_bills_dict'])
    except Exception as err:
      print('Could not save similarity: ' + str(err))
      raise err
    return bill


def get_bill_xml(congressDir: str, uscongress: bool = True) -> list:
  if not uscongress:
    return [file for file in os.listdir(congressDir) if file.endswith(".xml")]

  xml_files = list()
  USCONGRESS_XML_FILE = settings.USCONGRESS_XML_FILE
  for root, dirs, files in os.walk(congressDir):
    if USCONGRESS_XML_FILE in files:
      xml_path = os.path.join(root, USCONGRESS_XML_FILE)
      xml_files.append(xml_path)
  return xml_files

def filterLatestVersionOnly(billFiles: List[str]):
  # For bills that are not unique, get only the latest one
  # Filter to get just the path before /text-versions
  billPaths = list(map(lambda f: f.split('/text')[0], billFiles))
  print('Number of bills: ' + str(len(billPaths)))
  billPathsDupes = list(duplicates(billPaths))
  print('Number of bills with multiple versions: ' + str(len(billPathsDupes)))
  billPathsUnique = list(filter(lambda f: f not in billPathsDupes, billPaths)) 
  billFilesUnique = list(filter(lambda f: f.split('/text')[0] in billPathsUnique, billFiles))
  billNumbersDupes = list(set(filter(None, map(getBillNumberFromCongressScraperBillPath, billPathsDupes))))
  latestBillVersions = list(map(getLatestBillVersion, billNumbersDupes))
  print('Number of latestBillVersions: ' + str(len(latestBillVersions)))
  billFilesDupes = [ os.path.join(getBillPath(version), 'text-versions',re.sub(r'[0-9]+[a-z]+[0-9]+', '', version), 'document.xml') for i, version  in enumerate(latestBillVersions)]
  billFilesFiltered = billFilesUnique + billFilesDupes
  print('Number of bills (latest versions): ' + str(len(billFilesFiltered)))

  return billFilesFiltered

CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in range(117, 118)]
def processBills(congresses: list=CONGRESS_LIST_DEFAULT, docType: str='dtd', uscongress: bool=False):
  for congress in congresses:
    print('Finding Similarity congress: {0}'.format(congress))
    congressDir = getXMLDirByCongress(congress=congress, docType=docType, uscongress=uscongress)
    billFiles = get_bill_xml(congressDir=congressDir, uscongress=uscongress)
    if uscongress:
      billFiles = filterLatestVersionOnly(billFiles)
    for billFile in billFiles:
      if uscongress:
        billFilePath = billFile
      else:
        billFilePath = os.path.join(congressDir, billFile)
      print('Finding Similiarity {0}'.format(billFilePath))
      try:
        processBill(billFilePath)
      except Exception as err:
        print('Could not process for similarity: {0}'.format(str(err)))
        pass


def moreLikeThis(queryText: str, index: str='billsections'):
  query = constants.makeMLTQuery(queryText)
  return runQuery(index=index, query=query, size=MAX_BILLS_SECTION)

def printResults(res):
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

def getInnerHits(res):
  return res.get('hits').get('hits')

def getResultBillnumbers(res):
  return [hit.get('_source').get('billnumber') for hit in getInnerHits(res)]

def getInnerResults(res):
   return [hit.get('inner_hits') for hit in getInnerHits(res)]

def getSimilarBills(es_similarity: List[dict]) -> dict:
  """
  Get a dict of similar bills and matching sections
  Remove items from the 'similars' object which refer to the same bill section.
  Retain only the higest scoring match.

  Args:
      es_similarity (list[dict]): the es_similarity object generated by getSimilarSections 

  Returns:
      similarBills (dict): a dict of the form:
    {
      116hr1500: [
        {section_num: 4, section_header: 'Definitions', score: 48.76, 
        sectionIndex: [index of section from original bill] }, ...
      ]
    }
  """
  similarBills = {}
  sectionSimilars = [item.get('similars', []) for item in es_similarity]
  billnumbers = list(unique_everseen(flatten([[similarItem.get('billnumber') for similarItem in similars] for similars in sectionSimilars])))
  for billnumber in billnumbers:
    try:
      similarBills[billnumber] = []
      for sectionIndex, similarItem in enumerate(sectionSimilars):
        sectionBillItems = sorted(filter(lambda x: x.get('billnumber', '') == billnumber, similarItem), key=lambda k: k.get('score', 0), reverse=True)
        if sectionBillItems and len(sectionBillItems) > 0:
          for sectionBillItem in sectionBillItems:
            # Check if we've seen this billItem before and which has a higher score
            currentScore = sectionBillItem.get('score', 0)
            currentSection = sectionBillItem.get('section_num', '') + sectionBillItem.get('section_header', '')
            dupeIndexes = [similarBillIndex for similarBillIndex, similarBill in enumerate(similarBills.get(billnumber, [])) if (similarBill.get('section_num', '') + similarBill.get('section_header', '')) == currentSection]
            if not dupeIndexes:
              sectionBillItem['sectionIndex'] = str(sectionIndex)
              sectionBillItem['target_section_number'] = es_similarity[sectionIndex].get('section_number', '')
              sectionBillItem['target_section_header'] = es_similarity[sectionIndex].get('section_header', '')
              similarBills[billnumber].append(sectionBillItem)
              break
            elif  currentScore > similarBills[billnumber][dupeIndexes[0]].get('score', 0):
              del similarBills[billnumber][dupeIndexes[0]]
              similarBills[billnumber].append(sectionBillItem)
    except Exception as err:
      print(err)

  return similarBills 

def getSimilarSections(res):
  similarSections = []
  try:
    hits = getInnerHits(res)
    innerResults = getInnerResults(res)
    for index, hit in enumerate(hits):
      innerResultSections = getInnerHits(innerResults[index].get('sections'))
      billSource = hit.get('_source')
      title = ''
      dublinCore = ''
      dublinCores = billSource.get('dc', [])
      if dublinCores:
        dublinCore = dublinCores[0]

      titleMatch = re.search(r'<dc:title>(.*)?<', str(dublinCore))
      if titleMatch:
        title = titleMatch[1].strip()
      num = innerResultSections[0].get('_source', {}).get('section_number', '')
      if num:
        num = num + " "
      header = innerResultSections[0].get('_source', {}).get('section_header', '')
      match = {
        "bill_number_version": billSource.get('id', ''),
        "score": innerResultSections[0].get('_score', ''),
        "billnumber": billSource.get('billnumber', ''),
        "congress": billSource.get('_source', {}).get('congress', ''),
        "session": billSource.get('session', ''),
        "legisnum": billSource.get('legisnum', ''),
        "title": title,
        "section_num": num,
        "section_header": header,
        "date": billSource.get('date'),
      }
      similarSections.append(match)
    return similarSections 
  except Exception as err:
    print(err)
    return []
