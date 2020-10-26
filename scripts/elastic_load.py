import os
import json
import re
from lxml import etree
from elasticsearch import exceptions, Elasticsearch
es = Elasticsearch()
from collections import OrderedDict

try:
    from . import constants
except:
    import constants

bill_file = "BILLS-116hr1500rh.xml"
bill_file2 = "BILLS-116hr299ih.xml"
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)
PATH_BILLSECTIONS_JSON = os.path.join('..', 'elasticsearch', 'billsections_mapping.json') 

def getXMLDirByCongress(congress: str ='116', docType: str = 'dtd') -> str:
  return os.path.join(constants.PATH_TO_DATA_DIR, congress, docType)

def getMapping(map_path):
    with open(map_path, 'r') as f:
        return json.load(f)

BILLSECTION_MAPPING = getMapping(PATH_BILLSECTIONS_JSON)

def getText(item):
  if not item:
    return ''
  try:
    return item.text 
  except:
    return ''

def createIndex(index: str='billsections', body: dict=BILLSECTION_MAPPING, delete=False):
  if delete:
    try:
      es.indices.delete(index=index)
    except exceptions.NotFoundError:
      print('No index to delete: ' + index)

  es.indices.create(index=index, ignore=400, body=body)

def getBillNumberFromBillPath(bill_path: str):
  # e.g. [path]/116/dtd/BILLS-116hr1500rh.xml
  return re.sub(r'.*\/', '', bill_path).replace('BILLS-', '').replace('.xml', '')

def indexBill(bill_path: str=PATH_BILL):
  try:
    billTree = etree.parse(bill_path)
  except:
    raise Exception('Could not parse bill')
  dctitle = billTree.xpath('//dublinCore/dc:title')
  dctitle_text = getText(dctitle) 
  congress = billTree.xpath('//form/congress')
  congress_text = re.sub(r'[a-zA-Z ]+$', '', getText(congress))
  session = billTree.xpath('//form/session')
  session_text = re.sub(r'[a-zA-Z ]+$', '', getText(session))
  legisnum = billTree.xpath('//legis-num')
  legisnum_text = getText(legisnum)
  if congress and legisnum_text:
    billnumber_text = congress + legisnum_text.lower().replace('. ', '')
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
      'dctitle': dctitle_text,
      'legisnum': legisnum_text,
      'billnumber': billnumber_text,
      'headers': list(OrderedDict.fromkeys(headers_text)),
      'sections': [{
          'section_number': section.find('enum').text,
          'section_header':  section.find('header').text,
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode")
      } if (section.find('header').text and section.find('enum').text) else
      {
          'section_number': '',
          'section_header': '', 
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode")
      } 
      for section in sections ]
  } 

  res = es.index(index="billsections", body=doc)
  print(res['result'])

    # billRoot = billTree.getroot()
    # nsmap = {k if k is not None else '':v for k,v in billRoot.nsmap.items()}

CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in range(113, 116)]
def indexBills(congresses: list=CONGRESS_LIST_DEFAULT, docType: str='dtd'):
  for congress in congresses:
    print('Indexing congress' + congress)
    congressDir = getXMLDirByCongress(congress=congress, docType=docType) 
    billFiles = [file for file in os.listdir(congressDir) if file.endswith(".xml")]
    for billFile in billFiles:
      billFilePath = os.path.join(congressDir, billFile)
      print('Indexing' + billFilePath)
      try:
        indexBill(billFilePath)
      except:
        pass

def refreshIndices(index: str="billsections"):
  es.indices.refresh(index=index)

# res = es.search(index="billsections", body={"query": {"match_all": {}}})
def runQuery(index: str='billsections', query: dict=constants.SAMPLE_QUERY_NESTED_MLT_MARALAGO) -> dict:
  return es.search(index=index, body=query)

def printResults(res):
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

def getInnerResults(res):
   return [hit['inner_hits'] for hit in res['hits']['hits']]

if __name__ == "__main__": 
  createIndex(delete=True)
  indexBills()
  refreshIndices()
  res = runQuery()
  innerResults = getInnerResults(res)
  print(innerResults)