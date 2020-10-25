import os
import json
from lxml import etree
from elasticsearch import Elasticsearch
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

SAMPLE_QUERY = {
  "query": {
    "match": {
      "headers": {
        "query": "date"
      }
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

def getXMLDirByCongress(congress: str ='116', docType: str = 'dtd') -> str:
  return os.path.join(constants.PATH_TO_DATA_DIR, congress, docType)

def getMapping(map_path):
    with open(map_path, 'r') as f:
        return json.load(f)

BILLSECTION_MAPPING = getMapping(PATH_BILLSECTIONS_JSON)

def createIndex(index: str='billsections', body: dict=BILLSECTION_MAPPING, delete=False):
  if delete:
    es.indices.delete(index=index)
  es.indices.create(index=index, ignore=400, body=body)

def indexBill(bill_path):
  try:
    billTree = etree.parse(bill_path)
  except:
    raise Exception('Could not parse bill')
  sections = billTree.xpath('//section')
  headers = billTree.xpath('//header')
  from collections import OrderedDict
  headers_text = [ header.text for header in headers]

  # Uses an OrderedDict to deduplicate headers
  # TODO handle missing header and enum separately
  doc = {
      'headers': list(OrderedDict.fromkeys(headers_text)),
      'sections': [{
          'section_number': section.find('enum').text,
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode"),
          'section_header':  section.find('header').text
      } if section.find('header') and section.find('enum').text else
      {
          'section_number': '',
          'section_text': etree.tostring(section, method="text", encoding="unicode"),
          'section_xml': etree.tostring(section, method="xml", encoding="unicode"),
          'section_header': '' 
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

# res = es.search(index="billsections", body={"query": {"match_all": {}}})
def runQuery(index: str='billsections', query: dict=SAMPLE_QUERY_NESTED) -> dict:
  return es.search(index=index, body=SAMPLE_QUERY_NESTED)

def printResults(res):
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

def getInnerResults(res):
   return [hit['inner_hits'] for hit in res['hits']['hits']]

if __name__ == "__main__": 
  createIndex(delete=True)
  # indexBill(PATH_BILL)
  indexBills()
  refreshIndices()
  res = runQuery()
  innerResults = getInnerResults(res)
  print(innerResults[3])