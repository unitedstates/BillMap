import os
import json
import re
from lxml import etree
from elasticsearch import exceptions, Elasticsearch
es = Elasticsearch()
from collections import OrderedDict

from django.conf import settings
from common import constants

bill_file = "BILLS-116hr1500rh.xml"
bill_file2 = "BILLS-116hr299ih.xml"
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)

BASE_DIR = settings.BASE_DIR

def getXMLDirByCongress(congress: str ='116', docType: str = 'dtd', uscongress: bool = True) -> str:
  if uscongress:
    return os.path.join(BASE_DIR, 'congress', 'data', congress, 'bills')
  return os.path.join(constants.PATH_TO_DATA_DIR, congress, docType)

def getMapping(map_path):
    with open(map_path, 'r') as f:
        return json.load(f)

def getText(item):
  if item is None:
    return ''
  if isinstance(item, list):
    item = item[0]

  try:
    return item.text 
  except:
    return ''


def createIndex(index: str='billsections', body: dict=constants.BILLSECTION_MAPPING, delete=False):
  if delete:
    try:
      es.indices.delete(index=index)
    except exceptions.NotFoundError:
      print('No index to delete: {0}'.format(index))

  es.indices.create(index=index, ignore=400, body=body)

def getBillNumberFromBillPath(bill_path: str):
  # e.g. [path]/116/dtd/BILLS-116hr1500rh.xml
  return re.sub(r'.*\/', '', bill_path).replace('BILLS-', '').replace('.xml', '')

def indexBill(bill_path: str=PATH_BILL):
  try:
    billTree = etree.parse(bill_path)
  except:
    raise Exception('Could not parse bill')
  dublinCores = billTree.xpath('//dublinCore')
  if dublinCores and dublinCores[0]:
    dublinCore = etree.tostring(dublinCores[0], method="xml", encoding="unicode"),
  else:
    dublinCore = ''
  dctitle = getText(billTree.xpath('//dublinCore/dc:title', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}))
  billCongressTypeNumberVersion = '' 
  if dctitle and dctitle.find(':') > -1:
    billCongressTypeNumberVersion = dctitle.split(':')[0].replace(' ','').lower()
  congress = billTree.xpath('//form/congress')
  congress_text = re.sub(r'[a-zA-Z ]+$', '', getText(congress))
  session = billTree.xpath('//form/session')
  session_text = re.sub(r'[a-zA-Z ]+$', '', getText(session))
  legisnum = billTree.xpath('//legis-num')
  legisnum_text = getText(legisnum)
  if congress and legisnum_text:
    billnumber_text = congress_text + legisnum_text.lower().replace('. ', '')
  else:
    billnumber_text = getBillNumberFromBillPath(bill_path)
  sections = billTree.xpath('//section')
  headers = billTree.xpath('//header')
  from collections import OrderedDict
  headers_text = [ header.text for header in headers]

  # Uses an OrderedDict to deduplicate headers
  # TODO handle missing header and enum separately
  doc = {
      'congress': congress_text,
      'session': session_text,
      'dc': dublinCore,
      'legisnum': legisnum_text,
      'billnumber': billnumber_text,
      'billnumber_version': billCongressTypeNumberVersion,
      'headers': list(OrderedDict.fromkeys(headers_text)),
      'sections': [{
          'section_number': section.xpath('enum')[0].text,
          'section_header':  section.xpath('header')[0].text,
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode")
      } if (section.xpath('header') and len(section.xpath('header')) > 0  and section.xpath('enum') and len(section.xpath('enum'))>0) else
      {
          'section_number': '',
          'section_header': '', 
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode")
      } 
      for section in sections ]
  } 
  
  # If the document has no identifiable bill number, it will be indexed with a random id
  # This will make retrieval and updates ambiguous
  if billCongressTypeNumberVersion is not '' and len(billCongressTypeNumberVersion) > 7:
      doc['id'] = billCongressTypeNumberVersion 

  res = es.index(index="billsections", body=doc)
  return res

    # billRoot = billTree.getroot()
    # nsmap = {k if k is not None else '':v for k,v in billRoot.nsmap.items()}


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


CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in range(116, 117)]
def indexBills(congresses: list=CONGRESS_LIST_DEFAULT, docType: str='dtd', uscongress: bool=False):
  for congress in congresses:
    print('Indexing congress: {0}'.format(congress))
    congressDir = getXMLDirByCongress(congress=congress, docType=docType, uscongress=uscongress)
    billFiles = get_bill_xml(congressDir=congressDir, uscongress=uscongress)
    for billFile in billFiles:
      if uscongress:
        billFilePath = billFile
      else:
        billFilePath = os.path.join(congressDir, billFile)
      print('Indexing {0}'.format(billFilePath))
      try:
        indexBill(billFilePath)
      except Exception as err:
        print('Could not index: {0}'.format(str(err)))
        pass

def refreshIndices(index: str="billsections"):
  es.indices.refresh(index=index)

# res = es.search(index="billsections", body={"query": {"match_all": {}}})
def runQuery(index: str='billsections', query: dict=constants.SAMPLE_QUERY_NESTED_MLT_MARALAGO, size: int=10) -> dict:
  return es.search(index=index, body=query, size=size)

def moreLikeThis(queryText: str, index: str='billsections'):
  query = constants.makeMLTQuery(queryText)
  return runQuery(index=index, query=query)

def printResults(res):
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

def getHits(res):
  return res.get('hits').get('hits')

def getResultBillnumbers(res):
  return [hit.get('_source').get('billnumber') for hit in getHits(res)]

def getInnerResults(res):
   return [hit.get('inner_hits') for hit in getHits(res)]

def getSimilarSections(res):
  similarSections = []
  try:
    hits = getHits(res)
    innerResults = getInnerResults(res)
    for index, hit in enumerate(hits):
      innerResultSections = getHits(innerResults[index].get('sections'))
      billSource = hit.get('_source')
      title = ''
      dublinCore = ''
      dublinCores = billSource.get('dc', [])
      if dublinCores:
        dublinCore = dublinCores[0]

      titleMatch = re.search(r'<dc:title>(.*)?<', dublinCore)
      if titleMatch:
        title = titleMatch[1].strip()
      num = innerResultSections[0].get('_source', {}).get('section_number', '')
      if num:
        num = num + " "
      header = innerResultSections[0].get('_source', {}).get('section_header', '')
      match = {
        "score": innerResultSections[0].get('_score', ''),
        "billnumber": billSource.get('billnumber', ''),
        "congress": billSource.get('_source', {}).get('congress', ''),
        "session": billSource.get('session', ''),
        "legisnum": billSource.get('legisnum', ''),
        "title": title,
        "section_num": num,
        "section_header": header,
        "section_num_header": num + header, 
        "section_xml": innerResultSections[0].get('_source', {}).get('section_xml', ''),
        "section_text": innerResultSections[0].get('_source', {}).get('section_text', '')
      }
      similarSections.append(match)
    return similarSections 
  except Exception as err:
    print(err)
    return []

if __name__ == "__main__": 
  createIndex(delete=True)
  indexBills()
  refreshIndices()
  res = runQuery()
  billnumbers = getResultBillnumbers(res)
  print('Top matching bills: {0}'.format(', '.join(billnumbers)))
  innerResults = getInnerResults(res)
  print(innerResults)