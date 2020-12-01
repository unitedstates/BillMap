import os
import json
import re
from lxml import etree
from operator import itemgetter
from elasticsearch import exceptions, Elasticsearch
es = Elasticsearch()
from collections import OrderedDict

from common import constants
from bills.models import Bill

bill_file = "BILLS-116hr1500rh.xml"
bill_file2 = "BILLS-116hr299ih.xml"
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)

def getXMLDirByCongress(congress: str ='116', docType: str = 'dtd') -> str:
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
  congress = billTree.xpath('//form/congress')
  congress_text = re.sub(r'[a-zA-Z ]+$', '', getText(congress))
  session = billTree.xpath('//form/session')
  # session_text = re.sub(r'[a-zA-Z ]+$', '', getText(session))
  legisnum = billTree.xpath('//legis-num')
  legisnum_text = getText(legisnum)
  if congress and legisnum_text:
    billnumber_text = congress_text + legisnum_text.lower().replace('. ', '')
  else:
    billnumber_text = getBillNumberFromBillPath(bill_path)
  sections = billTree.xpath('//section')
  # headers = billTree.xpath('//header')
  # from collections import OrderedDict
  # headers_text = [ header.text for header in headers]

  # Uses an OrderedDict to deduplicate headers
  # TODO handle missing header and enum separately
  # doc = {
  #     'congress': congress_text,
  #     'session': session_text,
  #     'dc': dublinCore,
  #     'legisnum': legisnum_text,
  #     'billnumber': billnumber_text,
  #     'headers': list(OrderedDict.fromkeys(headers_text)),
  #     'sections': [{
  #         'section_number': section.xpath('enum')[0].text,
  #         'section_header':  section.xpath('header')[0].text,
  #         'section_text': etree.tostring(section, method="text", encoding="unicode"),
  #         'section_xml': etree.tostring(section, method="xml", encoding="unicode")
  #     } if (section.xpath('header') and len(section.xpath('header')) > 0  and section.xpath('enum') and len(section.xpath('enum'))>0) else
  #     {
  #         'section_number': '',
  #         'section_header': '', 
  #         'section_text': etree.tostring(section, method="text", encoding="unicode"),
  #         'section_xml': etree.tostring(section, method="xml", encoding="unicode")
  #     } 
  #     for section in sections ]
  # }

  qs_bill = Bill.objects.filter(bill_congress_type_number=billnumber_text)
  if qs_bill.exists():
    bill = qs_bill.first()
    es_similarity = list()

    for section in sections:
      section_item = dict()
      section_text = etree.tostring(section, method="text", encoding="unicode")
      section_item['section'] = section_text

      similarity = moreLikeThis(queryText=section_text)
      similar_sections = sorted(getSimilarSections(similarity), key=itemgetter('score'), reverse=True)
      section_item['similars'] = similar_sections
      es_similarity.append(section_item)

    bill.es_similarity = es_similarity
    bill.save(update_fields=['es_similarity'])


CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in range(113, 117)]
def indexBills(congresses: list=CONGRESS_LIST_DEFAULT, docType: str='dtd'):
  for congress in congresses:
    print('Finding Similarity congress: {0}'.format(congress))
    congressDir = getXMLDirByCongress(congress=congress, docType=docType) 
    billFiles = [file for file in os.listdir(congressDir) if file.endswith(".xml")]
    for billFile in billFiles:
      billFilePath = os.path.join(congressDir, billFile)
      print('Finding Similiarity {0}'.format(billFilePath))
      try:
        indexBill(billFilePath)
      except Exception as err:
        print('Could not index: {0}'.format(str(err)))
        pass

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
