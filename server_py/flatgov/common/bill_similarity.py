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

def runQuery(index: str='billsections', query: dict=constants.SAMPLE_QUERY_NESTED_MLT_MARALAGO, size: int=10) -> dict:
  query = query
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
  
def getLatestBillVersion(billnumber: str) -> str:
  """
  Find latest version in Elasticsearch

  Args:
      billnumber (str): billnumber (without version) 

  Returns:
      str: version (e.g. 'ih', 'eh', 'enr', etc.) 
  """
  bills = runQuery(index='billsections', query=setBillNumberQuery(billnumber))
  billversion = ''
  if bills.get('hits') and bills.get('hits').length > 0 and bills.get('hits')[0].get('fields'):
    tophit = bills.get('hits')[0].get('fields')
    billnumber = tophit.get('billnumber')[0] 
    billversion = tophit.get('billversion')

  return billversion

def getSimilarBills(es_similarity: list):
  similarBills = []
  sectionSimilars = [item.get('similars', []) for item in es_similarity]
  billnumbers = list(unique_everseen(flatten([[similarItem.get('billnumber') for similarItem in similars] for similars in sectionSimilars])))

  for billnumber in billnumbers:
    similarBill = {'billnumber': billnumber}
    maxItem = {}
    
    for similarItem in sectionSimilars:
      sectionMaxItem = None
      sectionMaxItems = sorted(filter(lambda x: x.get('billnumber', '') == billnumber, similarItem), key=lambda k: k.get('score', 0), reverse=True)
      if sectionMaxItems and len(sectionMaxItems) > 0:
        sectionMaxItem = sectionMaxItems[0]
      
      if sectionMaxItem is not None and sectionMaxItem > maxItem.get('score', 0):
        maxItem = sectionMaxItem
        maxItem['title_list'] = sectionMaxItem.get('title', [])
      
    similarBill['scores'].append(maxItem)

  return similarBills

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

    bill.es_similarity = es_similarity
    similar_bills = getSimilarBills(es_similarity)
    bill.save(update_fields=['es_similarity'])
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
  # TODO: For bills that are not unique, get only the latest one

  # Filter to get just the path before /text-versions
  billPaths = filter(lambda f: f.split('/text')[0], billFiles)
  billPathsUnique = list(unique_everseen(billPaths))
  billFilesFiltered = filter(lambda f: f.split('/text')[0] in billPathsUnique, billFiles)
  billPathsDupes = list(set(duplicates(billPaths)))
  billNumbersDupes = filter(None, map(getBillNumberFromCongressScraperBillPath, billPathsDupes))
  billVersions = map(getLatestBillVersion, billNumbersDupes)
  # Keep that one in the list
  # Add those to the billFilesFiltered

  return billFilesFiltered

CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in range(113, 118)]
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
        print('Could not index: {0}'.format(str(err)))
        pass


def moreLikeThis(queryText: str, index: str='billsections'):
  query = constants.makeMLTQuery(queryText)
  return runQuery(index=index, query=query)

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
