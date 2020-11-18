from json import dump
import sys
import os
import argparse
import logging
import re

from common.constants import PATH_TO_RELATEDBILLS_DIR, PATH_TO_NOYEAR_TITLES_INDEX
from common.utils import loadTitlesIndex, loadRelatedBillJSON, dumpRelatedBillJSON
from common.billdata import deep_get, billIdToBillNumber, loadJSON, loadDataJSON, loadBillsMeta

from bills.handler import BillDataHandler
from bills.models import Bill, Cosponsor

OF_YEAR_REGEX = re.compile(r'\sof\s[0-9]+$')

logging.basicConfig(filename='billdata.log', filemode='w', level='INFO')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

BILLS_META = loadBillsMeta()
ALL_BILLS = list(BILLS_META.keys())


# NOTE: This is very slow. Takes ~120 minutes for 111 - 116th Congress
def addSimilarTitles(noYearTitlesIndex: dict, billsRelated = {}):
    totalTitles = len(noYearTitlesIndex)
    titleNum = 0
    for title, bills in noYearTitlesIndex.items():
        titleNum += 1 
        logger.info('Adding noYearTitle: ' + title)
        logger.info(str(titleNum) +' of ' + str(totalTitles))
        relatedBills = { bill: loadRelatedBillJSON(bill) for bill in bills}
        relatedTitles = { bill: list(filter(lambda titleItem: titleItem.startswith(title), deep_get(BILLS_META, bill, 'titles'))) for bill in bills}
        for bill_outer in relatedBills:
            for bill_inner in relatedBills:
                similarTitle = relatedTitles.get(bill_inner)
                if similarTitle and len(similarTitle) == 1:
                    similarTitle = similarTitle[0]
                else:
                    continue
                # Find a matching item, if any, in the list billsRelated[bill_outer]
                if not deep_get(relatedBills, bill_outer, 'related', bill_inner):
                        relatedBills[bill_outer]['related'][bill_inner] = {
                            'titles_year': [similarTitle] 
                        }
                elif not deep_get(relatedBills, bill_outer, 'related', bill_inner, 'titles_year'):
                        relatedBills[bill_outer]['related'][bill_inner]['titles_year'] = [similarTitle]
                else:
                    if similarTitle not in relatedBills[bill_outer]['related'][bill_inner]['titles_year']:
                        try:
                            relatedBills[bill_outer]['related'][bill_inner]['titles_year'].append(similarTitle)
                        except:
                            relatedBills[bill_outer]['related'][bill_inner]['titles_year'] = [similarTitle]

                    if deep_get(relatedBills, bill_outer, 'related', bill_inner, 'titles_year'):
                        logger.debug(relatedBills[bill_outer]['related'][bill_inner])
            dumpRelatedBillJSON(bill_outer, relatedBills.get(bill_outer))
    logger.info('*** Finished Adding NoYear Titles ***')

def addSameTitles(titlesIndex: dict):
    for title, bills in titlesIndex.items():
        for bill_outer in bills:
            logger.debug('Adding related titles: ' + bill_outer)
            billRelated = loadRelatedBillJSON(bill_outer)
            for bill_inner in bills:
                # Find a matching item, if any, in the list billRelated
                if not deep_get(billRelated, 'related'):
                    billRelated['related'] = {}
                if not deep_get(billRelated, 'related', bill_inner):
                    billRelated['related'][bill_inner] = {'titles': [title]}
                elif title not in deep_get(billRelated, 'related', bill_inner, 'titles'):
                    billRelated['related'][bill_inner]['titles'].append(title)
            logger.debug('Saving with related titles: ' + bill_outer)
            dumpRelatedBillJSON(bill_outer, billRelated)
    logger.info('*** Finished Adding Same Titles ***')

def addGPORelatedBills():
    for bill_outer in ALL_BILLS:
        billRelated = loadRelatedBillJSON(bill_outer)
        billData = loadDataJSON(bill_outer)
        if not billData or not deep_get(billData, 'related_bills'):
            continue

        relatedBillItems = deep_get(billData, 'related_bills')

        for billItem in relatedBillItems:
            bill_inner = billIdToBillNumber(billItem.get('bill_id'))
            newDict = {'reason': billItem.get('reason'), 'identified_by': billItem.get('identified_by')}
            logger.debug(newDict)
            # Find a matching item, if any, in the list billsRelated[bill_outer]
            if not deep_get(billRelated, 'related', bill_inner):
                billRelated['related'][bill_inner] =  newDict
            else:
                billRelated['related'][bill_inner].update(newDict)
        dumpRelatedBillJSON(bill_outer, billRelated)


def addSponsors():
    for bill_outer in ALL_BILLS:

        billData = loadDataJSON(bill_outer)
        relatedBill = loadRelatedBillJSON(bill_outer)
        if not billData or not  relatedBill or not deep_get(billData, 'sponsor'):
            continue

        sponsorItem = deep_get(billData, 'sponsor')
        cosponsorItems = deep_get(billData, 'cosponsors')
        summary = billData.get('summary', {}).get('text')
        bill_type = billData.get('bill_type')
        congress = billData.get('congress')
        number = billData.get('number')
        short_title = billData.get('short_title')

        for bill_inner, relatedItemValue in relatedBill.get('related').items():
            billInnerData = loadDataJSON(bill_inner)
            if not billInnerData:
                continue
            relatedBill['summary'] = summary
            relatedBill['type'] = bill_type
            relatedBill['congress'] = congress
            relatedBill['number'] = number
            relatedBill['short_title'] = short_title

            relatedSponsorItem = deep_get(billInnerData, 'sponsor')
            if sponsorItem and relatedSponsorItem and sponsorItem.get('bioguide_id') == relatedSponsorItem.get('bioguide_id') and sponsorItem.get('name') == relatedSponsorItem.get('name'):
                relatedBill['related'][bill_inner]['sponsor'] = relatedSponsorItem 

            relatedCosponsorItems = deep_get(billInnerData, 'cosponsors')
            if cosponsorItems and relatedCosponsorItems:
                # Get cosponsorItems where name and bioguide match
                commonCosponsors = list(filter(lambda item: any(matchItem.get('bioguide_id') == item.get('bioguide_id') and matchItem.get('name') == item.get('name') for matchItem in cosponsorItems), relatedCosponsorItems))
                if commonCosponsors:
                    relatedBill['related'][bill_inner]['cosponsors'] = commonCosponsors 
        dumpRelatedBillJSON(bill_outer, relatedBill)

        try:
            bill_handler_obj = BillDataHandler(
                data=relatedBill, congress_type_num=bill_outer)
            bill_obj, created = Bill.objects.get_or_create(
                bill_congress_type_number=bill_outer,
                defaults=bill_handler_obj.bill
            )
            if not created:
                Bill.objects.filter(bill_congress_type_number=bill_outer).update(**bill_handler_obj.bill)
                logger.info(f'{bill_obj.bill_congress_type_number} - bill has updated.')
            else:
                logger.info(f'{bill_obj.bill_congress_type_number} - bill has created.')

            for item in bill_handler_obj.cosponsors:
                cosponsor_obj, created = Cosponsor.objects.get_or_create(
                    name=item.get('name'),
                    bioguide_id=item.get('bioguide_id'),
                )
                bill_obj.cosponsors.add(cosponsor_obj)
            logger.info(f'Cosponsors are added to bill - {bill_obj.bill_congress_type_number}.')
        except Exception as e:
            logger.info(f'Bill - {bill_outer} : {e}.')


def makeAndSaveRelatedBills(titlesIndex = loadTitlesIndex(), remake = False):
    if not os.path.isdir(PATH_TO_RELATEDBILLS_DIR):
        os.mkdir(PATH_TO_RELATEDBILLS_DIR)
    logger.info('Adding same titles')
    addSameTitles(titlesIndex=titlesIndex)
    logger.info('Adding similar titles')
    addSimilarTitles(noYearTitlesIndex=loadTitlesIndex(titleIndexPath=PATH_TO_NOYEAR_TITLES_INDEX))
    logger.info('Adding related bills from GPO data')
    addGPORelatedBills()
    logger.info('Adding sponsor info')
    addSponsors()
