from collections import Counter
from datetime import datetime
from operator import itemgetter
import re
from typing import List

from django.db import models
from django.conf import settings
from iteration_utilities import flatten
from django.utils.translation import gettext_lazy as _

from bills.templatetags.bill_filters import stagesFormat

MAX_RELATED_BILLS = 30
MAX_SORT_SCORE = 100000

def sortRelatedBills(bill: dict) -> int:
    sortScore = 0
    if 'identical' in bill.get('reason', ''):
        sortScore = MAX_SORT_SCORE
    elif 'title match' in bill.get('reason', ''):
        sortScore = MAX_SORT_SCORE - 100
    else:
        sortScore = bill.get('score', 0)
    return sortScore

def cleanReason(reason: str) ->  str:
    """
    Converts data form of similarity reason (e.g. `bills-nearly_identical`) to a more readable form (e.g. `nearly identical`)

    Args:
        reason (str): The similarity reason in its data form 

    Returns:
        (str): The similarity reason in its readable form
    """
    r1 = re.sub(r'bills-',r'', reason)
    r2 = re.sub(r'_([a-z]*)_([a-z]*)_',r'\1 \2', r1)
    return r2.replace('_', ' ').replace('match main', 'match (main)')

def cleanReasons(reasons: List[str]) -> List[str]:
    """
    Converts a List of strings of similarity reasons (e.g. [`bills-nearly_identical`...]) to a more readable form (e.g. [`nearly identical`...])
    If both 'identical' and 'nearly identical' are listed, removes 'nearly identical'. Also removes 'some similarity'.

    Args:
        reasons (List[str]): list of reasons in data form 

    Returns:
        (List[str]): list of reasons in readable form
    """
    reasons = [cleanReason(reason) for reason in reasons if reason not in [None, 'bills-some_similarity']]
    if 'identical' in reasons and 'nearly identical' in reasons:
        reasons.remove('nearly identical')
    if reasons and len(reasons) > 0:
       return reasons
    else:
        return []

def getReasonString(reasons: List[str]) -> str:
    """
    Generates a comma-separated string of reasons a formin readable form from a list of reasons in dat

    Args:
        reasons (List[str]): list of reasons in data form

    Returns:
        str: comma-separated string of reasons in readable form 
    """
    # TODO: consider sorting the reasons in a particular order
    return ', '.join(sorted(list(dict.fromkeys(cleanReasons(reasons)))))
class Bill(models.Model):
    bill_congress_type_number = models.CharField(max_length=100, unique=True, db_index=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    congress = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=5, null=True, blank=True)
    titles = models.JSONField(default=list)
    summary = models.TextField(null=True, blank=True)
    titles_whole_bill = models.JSONField(default=list)
    short_title = models.TextField(null=True, blank=True)
    sponsor = models.JSONField(default=dict, blank=True)
    cosponsors = models.ManyToManyField(
        'bills.Cosponsor', blank=True)
    related_bills = models.JSONField(default=list, blank=True)
    related_dict = models.JSONField(default=dict)
    cosponsors_dict = models.JSONField(default=list, blank=True)
    committees_dict = models.JSONField(default=list, blank=True)
    es_similarity = models.JSONField(default=list, blank=True)
    es_similar_reasons = models.JSONField(default=dict, blank=True)
    es_similar_bills_dict = models.JSONField(default=dict, blank=True, null=True)
    became_law = models.BooleanField(default=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bill_congress_type_number

    @property
    def title(self) -> str:
        if self.short_title:
            return self.short_title 
        else:
            if self.titles_whole_bill and len(self.titles_whole_bill) > 0:
                return self.titles_whole_bill[0] 
        return ''


    @property
    def type_abbrev(self) -> str:
        if self.type:
            return stagesFormat.get(self.type.upper(), '')
        else:
            return ''

    @property
    def became_law_through_related_bill(self):
        if self.became_law:
            return 'This bill became law'
        for related_bill in self.get_related_bill_numbers():
            try:
                bill = Bill.objects.get(bill_congress_type_number=related_bill)

                if bill.became_law:
                    return {"bill_number": related_bill, "message":'This bill became law through a related bill, '}
            except:
                return None
        return None

    def get_related_bill_numbers(self):
        return self.related_dict.keys()

    def get_cosponsor_bill(self, name):
        result = list()
        related_dict = self.related_dict
        for congress, value in related_dict.items():
            if type(value) is not dict or not value.get('cosponsors'):
                continue
            if congress == self.bill_congress_type_number:
                continue
            congress_list = [item.get('name') \
                for item in value.get('cosponsors') if item.get('name')]
            if name in congress_list:
                result.append(congress)
            else:
                continue
        return result



    @property
    def get_similar_bills(self):
        """
        Gets a list of bills that is displayed in the 'Related Bills' table
        This combines various JSON fields from the Bill.object, each of which
        is a dict of similar bills, with reasons for the similarity

        Combine bills from:
         - related_dict (including title reasons)
         - es_similar_bills_dict, enriched with reasons from es_similar_reasons

        Returns:
            List[similar bill dict]: List of dicts of similar bills

            Each similar bill dict is of the form (additional bill_dict fields in comments):
            { "116hr200": {
                "bill_id" # (bill_dict)
                "bill_congress_type_number": billnumber,
                "type"  # (bill_dict)
                "identified_by"
                "reason"
                "score" # (similar_bill_dict)
                "number_of_sections" #  (similar_bill_dict)
                "max_item" #  (similar_bill_dict)
                "title_max" #  (similar_bill_dict)
                "in_db" #  (similar_bill_dict)
                "titles"  # (bill_dict)
                "titles_whole_bill"  # (bill_dict)
                "title_whole_bill"  # (bill_dict)
                // BillMap reasons include 'identical', 'nearly identical', 'section similarity', 'title match', 'title match (main)'
                // CRS reasons include 'related' and 'procedurally related' 
                }
        """


        billnumbers_all = list()

        related_bills = dict()
        for bill_congress_type_number, bill in self.related_dict.items():
            bill_dict = bill
            """
            This has the following fields:
            bill_dict = {
                "bill_id": "hr529-116", 
                "bill_congress_type_number": "116hr529"
                "type": "", 
                "identified_by": "BillMap", 
                "reason": "bills-title_match_main, bills-title_match", 
                # "score" set to 99 to put these at the top (similar_bill_dict) 
                # number_of_sections (similar_bill_dict)
                # "max_item" (similar_bill_dict)
                # "title_max" (similar_bill_dict)
                # "in_db" (similar_bill_dict)
                # "title" (similar_bill_dict)
                "titles"
                "titles_whole_bill": ["To direct the Secretary of Transportation to establish a national intersection and interchange safety construction program, and for other purposes.", "National Intersection and Interchange Safety Construction Program Act"], 
                "title_whole_bill": ", ".join(bill.get('titles_whole_bill')) 
            }
            In addition, we add a score (int or float) and string fields "title" and "title_whole_bill"
            """
            if type(bill_dict) is not dict:
                continue
            if not bill_dict.get('bill_congress_type_number'):
                bill_dict['bill_congress_type_number'] = bill_congress_type_number

            # This is here to ensure that all original 'related dict' items are shown in the final output
            # TODO: it may be better to do this with a separate flag
            bill_dict['score'] = 99
            if bill.get('titles'):
                bill_dict['title'] = ", ".join(bill.get('titles'))
            if bill.get('titles_whole_bill'):
                bill_dict['title__whole_bill'] = ", ".join(bill.get('titles_whole_bill'))
            if bill_congress_type_number == self.bill_congress_type_number:
                reasons = bill.get('reason', '').split(', ')
                reasonString = getReasonString(['identical', *reasons])
                bill['reason'] = reasonString 
                bill_dict['reason'] = reasonString 
            else:
                bill_dict['reason'] = getReasonString(bill.get('reason').split(', '))
            qs_bill = Bill.objects.filter(
                bill_congress_type_number=bill_congress_type_number)
            bill_dict['in_db'] = qs_bill.exists(),

            related_bills[bill_congress_type_number] = bill_dict
            billnumbers_all.append(bill_congress_type_number)

        # Creates a 'similar_bills' list and adds items based on the total section score
        # Each Item is of the form:
        #    { "116hr200": {
        #        # "bill_id" (bill_dict)
        #        "bill_congress_type_number": billnumber,
        #        # "type"  (bill_dict)
        #        "identified_by": "BillMap"
        #        "reason": "nearly identical, title match, title match (main)" 
        #        "score": sum([item.get("score", 0) for item in similarBillItem]),
        #        "number_of_sections": len(similarBillItem),
        #        "max_item": maxItem,
        #        "title_max": maxItem.get("title", ""), # This is of the form "116 HR 529 IH: National Intersection and Interchange Safety Construction Program Act of 2019" and is taken from the bill metadata
        #        "in_db": qs_bill.exists(),
        #        # "titles"  (bill_dict)
        #        # "titles_whole_bill"  (bill_dict)
        #        # "title_whole_bill"  (bill_dict)
        #        // BillMap reasons include 'identical', 'nearly identical', 'some similarity', 'section similarity', 'unrelated' 'title match', 'title match (main)'
        #        // CRS reasons include 'related' and 'procedurally related' 
        #        }
        similar_bills = dict()
        for billnumber, similarBillItem in self.es_similar_bills_dict.items():
            qs_bill = Bill.objects.filter(
                bill_congress_type_number=billnumber)
            if similarBillItem:
                maxItem = sorted(similarBillItem, key=lambda k: k['score'], reverse=True)[0]
            else:
                maxItem = {}
            # Add reasons from es_similar_reasons
            reasonItem = self.es_similar_reasons.get(billnumber, '')
            reason = ''
            if reasonItem and reasonItem.get('Explanation'):
                # Do not include bills that are unrelated
                if reasonItem.get('Explanation') == "bills-unrelated":
                    continue
                reason = getReasonString([reasonItem.get('Explanation'), 'bills-section_similarity'])
            else:
                reason = 'section similarity'

            similar_bills[billnumber]={
                'score': sum([item.get('score', 0) for item in similarBillItem]),
                'number_of_sections': len(similarBillItem),
                'in_db': qs_bill.exists(),
                'title_max': maxItem.get('title', ''), 
                'bill_congress_type_number': billnumber,
                'max_item': maxItem,
                'reason': reason,
            }
            billnumbers_all.append(billnumber)
        
        # Combine bills from related_bills and similar_bills, 
        combined_related_bills = {}
        for billnumber in billnumbers_all:
            combined_related_bills[billnumber] = {
            }

            if related_bills.get(billnumber):
                combined_related_bills[billnumber] = related_bills[billnumber]
            elif similar_bills.get(billnumber):
                combined_related_bills[billnumber] = similar_bills[billnumber]
            
            if related_bills.get(billnumber) and similar_bills.get(billnumber):
                # merge common fields reason and identified_by
                combined_related_bills[billnumber]["score"] = max(related_bills[billnumber].get("score", 0), similar_bills[billnumber].get("score", 0))
                combined_related_bills[billnumber]["number_of_sections"] = similar_bills[billnumber].get("number_of_sections", 0)
                combined_related_bills[billnumber]["reason"] = getReasonString(related_bills.get(billnumber, {}).get("reason", "").split(", ") + similar_bills.get(billnumber, {}).get("reason", "").split(", "))
                combined_related_bills[billnumber]["identified_by"] = ", ".join(list(set(related_bills.get("identified_by", "").split(", ") + related_bills.get("identified_by", "").split(", "))))

        combined_related_bills_list = [bill for bill in combined_related_bills.values()]

        # Sort by score; insert the current bill at the front
        combined_related_bills_list = sorted(combined_related_bills_list, key=lambda k: k.get("score", 0), reverse=True)
        self_index = next((index for (index, d) in enumerate(combined_related_bills_list) \
            if d["bill_congress_type_number"] == self.bill_congress_type_number), None)
        if self_index:
            combined_related_bills_list.insert(0, combined_related_bills_list.pop(self_index))

        return  combined_related_bills_list[:MAX_RELATED_BILLS]

    @property
    def bill_summary(self):
        if not self.summary:
            return settings.BILL_SUMMARY_DEFAULT_TEXT
        return self.summary


class Cosponsor(models.Model):
    name = models.CharField(max_length=250) # Last, First 
    name_first = models.CharField(max_length=250, blank=True, null=True)
    name_last = models.CharField(max_length=250, blank=True, null=True)
    name_full_official = models.CharField(max_length=250, blank=True, null=True)
    bioguide_id = models.CharField(max_length=100, blank=True, null=True)
    thomas = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    type = models.CharField(max_length=3, blank=True, null=True)
    leadership = models.JSONField(default=list, blank=True, null=True) #list of terms in Leadership, with position; not everyone will have this item
    terms = models.JSONField(default=list)
    committees = models.JSONField(default=list, blank=True, null=True) #list of objects of the form {'thomas_id':x, 'rank':x, 'party': x}


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} - {self.name}'

    class Meta:
        unique_together = ('name', 'bioguide_id')
class Committee(models.Model):
    thomas_id = models.CharField(max_length=10, unique=True, db_index=True)
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    url = models.URLField(blank=True, null=True)
    minority_url = models.URLField(blank=True, null=True)
    house_committee_id = models.CharField(max_length=10, blank=True, null=True)
    jurisdiction = models.CharField(max_length=250, blank=True, null=True)
    cosponsors = models.ManyToManyField(
        'bills.Cosponsor', blank=True)

class Statement(models.Model):
    bill_number = models.CharField(max_length=127)
    bill_id = models.CharField(max_length=127, null=True, blank=True)
    bill_title = models.TextField(null=True, blank=True)
    congress = models.CharField(max_length=10)
    date_issued = models.CharField(max_length=35)
    permanent_pdf_link = models.CharField(max_length=255, null=True, blank=True)
    original_pdf_link = models.CharField(max_length=255, null=True, blank=True)
    administration = models.CharField(max_length=100,default='common')

    date_fetched = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.bill_number} - {self.permanent_pdf_link}'

    @property
    def get_permanent_pdf_link(self):
        if self.permanent_pdf_link:
            if self.permanent_pdf_link.startswith('http'):
                return self.permanent_pdf_link
            return '/media/'+self.permanent_pdf_link
        return None


class CboReport(models.Model):
    pub_date = models.CharField(max_length=50)
    title = models.CharField(max_length=1000)
    original_pdf_link = models.CharField(max_length=255)
    congress = models.CharField(max_length=55)
    bill_number = models.CharField(max_length=127)
    bill_id = models.CharField(max_length=127, null=True, blank=True)

    date_fetched = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.bill_number} - {self.original_pdf_link}'


class CommitteeDocument(models.Model):
    title = models.TextField()
    bill_number = models.CharField(max_length=127, null=True, blank=True)
    chamber = models.CharField(max_length=127, null=True, blank=True)
    category = models.CharField(max_length=127)
    committee = models.CharField(max_length=500)
    report_number = models.CharField(max_length=500)
    associated_legislation = models.CharField(max_length=500)
    original_pdf_link = models.CharField(max_length=500)
    report_type = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    congress = models.CharField(max_length=127, null=True, blank=True)
    request_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.original_pdf_link} {self.congress} {self.bill_number}"


#class PressStatement(models.Model):
#    url = models.CharField(max_length=1000)
#    date = models.CharField(max_length=500)
#    title = models.TextField()
#    statement_type = models.CharField(max_length=500)
#    member_id = models.CharField(max_length=500)
#    congress = models.CharField(max_length=127)
#    member_uri = models.CharField(max_length=1000)
#    name = models.CharField(max_length=127, null=True, blank=True)
#    chamber = models.CharField(max_length=127, null=True, blank=True)
#    state = models.CharField(max_length=127, null=True, blank=True)
#    party = models.CharField(max_length=127, null=True, blank=True)
#    bill_number = models.CharField(max_length=127)




    def __str__(self):
        return f'{self.congress} {self.bill_number}, {self.url}'

from celery import states

ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))

#class PressStatementTask(models.Model):
#    congress = models.CharField(max_length = 127)
#    bill_number = models.CharField(max_length=127)
#    status = models.CharField(
#        max_length=50, default=states.PENDING, db_index=True,
#        choices=TASK_STATE_CHOICES,
#        verbose_name=_('Task State'),
#        help_text=_('Current state of the press statement task.')
#    )
#    task_id = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
#
#    created_at = models.DateTimeField(auto_now=True)
#    updated_at = models.DateTimeField(auto_now_add=True)
    

#    def __str__(self):
#        return f"{self.congress} {self.bill_number} {self.status}"
