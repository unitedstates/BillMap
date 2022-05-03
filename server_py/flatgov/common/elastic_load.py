import os
import json
import re

from datetime import datetime
from lxml import etree
from django.conf import settings
from elasticsearch import exceptions, Elasticsearch

from common import constants
from common.utils import getText, getBillNumberFromBillPath, getBillNumberFromCongressScraperBillPath

es = Elasticsearch()

bill_file = "BILLS-116hr1500rh.xml"
bill_file2 = "BILLS-116hr299ih.xml"
PATH_BILL = os.path.join(constants.PATH_TO_CONGRESSDATA_XML_DIR, bill_file)

BASE_DIR = settings.BASE_DIR


def getXMLDirByCongress(congress: str = '117', docType: str = 'dtd', uscongress: bool = True) -> str:
    if uscongress:
        return os.path.join(BASE_DIR, 'congress', 'data', congress, 'bills')
    return os.path.join(constants.PATH_TO_DATA_DIR, congress, docType)


def getMapping(map_path: str) -> dict:
    with open(map_path, 'r') as f:
        return json.load(f)


# For future possible improvements, see https://www.is.inf.uni-due.de/bib/pdf/ir/Abolhassani_Fuhr_04.pdf
# Applying the Divergence From Randomness Approach for Content-Only Search in XML Documents
def createIndex(index: str = 'billsections', body: dict = constants.BILLSECTION_MAPPING, delete=False):
    if delete:
        try:
            es.indices.delete(index=index)
        except exceptions.NotFoundError:
            print('No index to delete: {0}'.format(index))

    print('Creating index with mapping: ')
    print(str(body))
    es.indices.create(index=index, ignore=400, body=body)


def getEnum(section) -> str:
    enumpath = section.xpath('enum')
    if len(enumpath) > 0:
        return enumpath[0].text
    return ''


def getHeader(section) -> str:
    headerpath = section.xpath('header')
    if len(headerpath) > 0:
        return headerpath[0].text
    return ''


def indexBill(bill_path: str = PATH_BILL, index_types: list = ['sections']):
    """
    Index bill with Elasticsearch

    Args:
        bill_path (str, optional): location of the bill xml file. Defaults to PATH_BILL.
        index_types (list, optional): Index by 'sections', 'bill_full' or both. Defaults to ['sections'].

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    try:
        billTree = etree.parse(bill_path)
    except:
        raise Exception('Could not parse bill')
    dublinCores = billTree.xpath('//dublinCore')
    if (dublinCores is not None) and (len(dublinCores) > 0):
        dublinCore = etree.tostring(dublinCores[0], method="xml", encoding="unicode"),
    else:
        dublinCore = ''
    dcdate = getText(billTree.xpath('//dublinCore/dc:date', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}))
    # TODO find date for enr bills in the bill status (for the flat congress directory structure)
    if (dcdate is None or len(dcdate) == 0) and '/data.xml' in bill_path:
        metadata_path = bill_path.replace('/data.xml', '/data.json')
        try:
            with open(metadata_path, 'rb') as f:
                metadata = json.load(f)
                dcdate = metadata.get('issued_on', None)
        except:
            pass
    if dcdate is None or len(dcdate) == 0:
        dcdate = None

    congress = billTree.xpath('//form/congress')
    congress_text = re.sub(r'[a-zA-Z ]+$', '', getText(congress))
    session = billTree.xpath('//form/session')
    session_text = re.sub(r'[a-zA-Z ]+$', '', getText(session))
    legisnum = billTree.xpath('//legis-num')
    legisnum_text = getText(legisnum)
    billnumber_version = getBillNumberFromCongressScraperBillPath(bill_path)
    print('billnumber_version: ' + billnumber_version)
    if billnumber_version == '':
        billnumber_version = getBillNumberFromBillPath(bill_path)
    dctitle = getText(billTree.xpath('//dublinCore/dc:title', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}))

    doc_id = ''
    billMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber_version)
    billversion = ''
    billnumber = ''
    if billMatch:
        billMatchGroup = billMatch.groupdict()
        billnumber = billMatchGroup.get('congress', '') + billMatchGroup.get('stage', '') + billMatchGroup.get('number', '')
        billversion = billMatchGroup.get('version', '')
    sections = billTree.xpath('//section')
    headers = billTree.xpath('//header')
    from collections import OrderedDict
    headers_text = [header.text for header in headers]

    # Uses an OrderedDict to deduplicate headers
    # TODO handle missing header and enum separately
    if 'sections' in index_types:
        doc = {
            'id': billnumber_version,
            'congress': congress_text,
            'session': session_text,
            'dc': dublinCore,
            'dctitle': dctitle,
            'date': dcdate,
            'legisnum': legisnum_text,
            'billnumber': billnumber,
            'billversion': billversion,
            'headers': list(OrderedDict.fromkeys(headers_text)),
            'sections': [{
                             'section_number': getEnum(section),
                             'section_header': getHeader(section),
                             'section_text': etree.tostring(section, method="text", encoding="unicode"),
                             'section_xml': etree.tostring(section, method="xml", encoding="unicode")
                         } if (
                        section.xpath('header') and len(section.xpath('header')) > 0 and section.xpath('enum') and len(
                    section.xpath('enum')) > 0) else
                         {
                             'section_number': '',
                             'section_header': '',
                             'section_text': etree.tostring(section, method="text", encoding="unicode"),
                             'section_xml': etree.tostring(section, method="xml", encoding="unicode")
                         }
                         for section in sections]
        }

        # If the document has no identifiable bill number, it will be indexed with a random id
        # This will make retrieval and updates ambiguous
        if doc_id != '' and len(doc_id) > 7:
            doc['id'] = doc_id

        res = es.index(index="billsections", body=doc)

    if 'bill_full' in index_types:
        billText = etree.tostring(billTree, method="text", encoding="unicode")
        doc_full = {
            'id': billnumber_version,
            'congress': congress_text,
            'session': session_text,
            'dc': dublinCore,
            'dctitle': dctitle,
            'date': dcdate,
            'legisnum': legisnum_text,
            'billnumber': billnumber,
            'billversion': billversion,
            'headers': list(OrderedDict.fromkeys(headers_text)),
            'billtext': billText
        }
        res = es.index(index="bill_full", body=doc_full)
    return

    # billRoot = billTree.getroot()
    # nsmap = {k if k is not None else '':v for k,v in billRoot.nsmap.items()}


def get_bill_xml(congressDir: str, uscongress: bool = True) -> list:
    if not uscongress:
        return [file for file in os.listdir(congressDir) if file.endswith(".xml")]

    xml_files = list()
    USCONGRESS_XML_FILE = settings.USCONGRESS_XML_FILE
    for root, _, files in os.walk(congressDir):
        if USCONGRESS_XML_FILE in files:
            xml_path = os.path.join(root, USCONGRESS_XML_FILE)
            xml_files.append(xml_path)
    return xml_files


CONGRESS_LIST_DEFAULT = [str(congressNum) for congressNum in
                         range(constants.CURRENT_CONGRESS, (constants.CURRENT_CONGRESS - 4), -1)]


def indexBills(congresses: list = CONGRESS_LIST_DEFAULT, docType: str = 'dtd', uscongress: bool = False,
               index_types: list = ['sections']):
    number_of_bills_total = 0
    for congress in congresses:
        print(str(datetime.now()) + ' - Indexing congress: {0}'.format(congress))
        congressDir = getXMLDirByCongress(congress=congress, docType=docType, uscongress=uscongress)
        billFiles = get_bill_xml(congressDir=congressDir, uscongress=uscongress)
        number_of_bills = 0
        for billFile in billFiles:
            if uscongress:
                billFilePath = billFile
            else:
                billFilePath = os.path.join(congressDir, billFile)
            print('Indexing {0}'.format(billFilePath))
            try:
                indexBill(bill_path=billFilePath, index_types=index_types)
                number_of_bills += 1
                if number_of_bills % 200 == 0:
                    print('Indexed ' + str(number_of_bills) + ' bills')
            except Exception as err:
                print('Could not index: {0}'.format(str(err)))
                pass
        print(str(datetime.now()) + ' - Finished indexing bills for Congress: ' + str(congress))
        print('Indexed ' + str(number_of_bills) + ' bills')
        number_of_bills_total += number_of_bills
    print(str(datetime.now()) + ' - Finished indexing bills for all Congresses: ' + str(', '.join(congresses)))
    print('Indexed ' + str(number_of_bills_total) + ' bills')


def refreshIndices(index: str = "billsections"):
    es.indices.refresh(index=index)


# res = es.search(index="billsections", body={"query": {"match_all": {}}})
def runQuery(index: str = 'billsections', query: dict = constants.SAMPLE_QUERY_NESTED_MLT_MARALAGO,
             size: int = 10) -> dict:
    return es.search(index=index, body=query, size=size)


def moreLikeThis(queryText: str, index: str = 'billsections'):
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


def getSimilarSections(res) -> list:
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

            titleMatch = re.search(r'<dc:title>(.*)?<', str(dublinCore))
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
