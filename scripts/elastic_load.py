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
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)
PATH_BILLSECTIONS_JSON = os.path.join('..', 'elasticsearch', 'billsections_mapping.json') 

def getMapping(map_path):
    with open(map_path, 'r') as f:
        return json.load(f)

BILLSECTION_MAPPING = getMapping(PATH_BILLSECTIONS_JSON)

es.indices.create(index='billsections', ignore=400, body=BILLSECTION_MAPPING)

def indexBill(bill_path):
    billTree = etree.parse(bill_path)
    sections = billTree.xpath('//section')
    headers = billTree.xpath('//header')
    from collections import OrderedDict
    headers_text = [ header.text for header in headers]

    # Uses an OrderedDict to deduplicate headers
    doc = {
        'headers': list(OrderedDict.fromkeys(headers_text)),
        'sections': [{
            'section_number': section.find('enum').text,
            'section_text': etree.tostring(section, method="text", encoding="unicode"),
            'section_xml': etree.tostring(section, method="xml", encoding="unicode"),
            'section_header':  section.find('header').text
        } for section in sections]
    } 

    res = es.index(index="billsections", body=doc)
    print(res['result'])

    # billRoot = billTree.getroot()
    # nsmap = {k if k is not None else '':v for k,v in billRoot.nsmap.items()}

es.indices.refresh(index="billsections")

# res = es.search(index="billsections", body={"query": {"match_all": {}}})

body = {
  "query": {
    "match": {
      "headers": {
        "query": "date"
      }
    }
  }
}

body_nested = {
  "query": {
    "nested": {
      "path": "sections",
      "query": {
        "bool": {
          "must": [
            { "match": { "sections.section_header": "date" }}
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

# res = es.search(index="billsections", body={"query": {"match_all": {}}})
res = es.search(index="billsections", body=body_nested)

def printResults(res):
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

def getInnerResults(res):
   return [hit['inner_hits'] for hit in res['hits']['hits']]
    