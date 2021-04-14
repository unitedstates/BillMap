from collections import Counter
from datetime import datetime
from operator import itemgetter

from django.db import models
from django.conf import settings
from iteration_utilities import flatten
from django.utils.translation import gettext_lazy as _

MAX_RELATED_BILLS = 30

class Bill(models.Model):
    bill_congress_type_number = models.CharField(max_length=100, unique=True, db_index=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    congress = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=5, null=True, blank=True)
    titles = models.JSONField(default=list)
    summary = models.TextField(null=True, blank=True)
    titles_whole_bill = models.JSONField(default=list)
    short_title = models.TextField(null=True, blank=True)
    sponsor = models.JSONField(default=dict)
    cosponsors = models.ManyToManyField(
        'bills.Cosponsor', blank=True)
    related_bills = models.JSONField(default=list)
    related_dict = models.JSONField(default=dict)
    cosponsors_dict = models.JSONField(default=list)
    committees_dict = models.JSONField(default=list)
    es_similarity = models.JSONField(default=list)
    es_similar_bills_dict = models.JSONField(default=dict)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bill_congress_type_number

    def get_type_abbrev(self) -> str:
        return ''.join([letter.upper() + '.' for letter in self.type])

    def get_related_bill_numbers(self):
        return self.related_dict.keys()

    def get_cosponsor_bill(self, name):
        result = list()
        related_dict = self.related_dict
        for congress, value in related_dict.items():
            if not value.get('cosponsors'):
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
        res = list()
        for billnumber, similarBillItem in self.es_similar_bills_dict.items():
            qs_bill = Bill.objects.filter(
                bill_congress_type_number=billnumber)
            if similarBillItem:
                maxItem = sorted(similarBillItem, key=lambda k: k['score'], reverse=True)[0]
            else:
                maxItem = {}
            res.append({
                'score': sum([item.get('score', 0) for item in similarBillItem]),
                'number_of_sections': len(similarBillItem),
                'in_db': qs_bill.exists(),
                'title_list': maxItem.get('title', ''),
                'bill_congress_type_number': billnumber,
                'max_item': maxItem,
                'reason': 'section match',
            })

        similar_bills = sorted(res, key=lambda k: k['score'], reverse=True)
        similar_bill_numbers = [bill.get('bill_congress_type_number') for bill in similar_bills]
        related_bills = list()
        
        for bill_congress_type_number, bill in self.related_dict.items():
            if bill_congress_type_number in similar_bill_numbers:
                bill_dict = similar_bills[similar_bill_numbers.index(bill_congress_type_number)]
                reason = f"{bill.get('reason')}, section match"
                
                # Deduplicate and remove 'None'
                bill_dict['reason'] = ', '.join(list(set([reasonItem for reasonItem in reason.split(', ') if reasonItem != 'None'])))
                bill_dict['identified_by'] = bill.get('identified_by')

                if bill_congress_type_number == self.bill_congress_type_number:
                    bill_dict['reason'] = 'identical, section match'
            else:
                bill_dict = bill
                bill_dict['bill_congress_type_number'] = bill_congress_type_number
                bill_dict['score'] = 0
                if bill.get('titles'):
                    bill_dict['title'] = ", ".join(bill.get('titles'))
            related_bills.append(bill_dict)

        sorted_related_bills = sorted(related_bills, key=lambda k: k['score'], reverse=True)
        self_index = next((index for (index, d) in enumerate(sorted_related_bills) \
            if d["bill_congress_type_number"] == self.bill_congress_type_number), None)
        if self_index:
            sorted_related_bills.insert(0, sorted_related_bills.pop(self_index))

        filtered_similar_bills = [bill for bill in similar_bills \
            if bill.get('bill_congress_type_number') not in self.related_dict.keys()]
        
        combined_related_bills = sorted_related_bills + filtered_similar_bills

        return combined_related_bills[:MAX_RELATED_BILLS]

    def get_second_similar_bills(self, second_bill):
        res = list()
        dup_checker_list = list()

        for item in self.es_similarity:
            similars = item.get('similars')
            target_billnumber = item.get('billnumber')
            target_section_header = item.get('section_header')
            if target_section_header:
                target_section_header = ' '.join(target_section_header.split())
            target_section_number = item.get('section_number')
            dup_checker = target_billnumber + target_section_header

            if not similars:
                continue

            for similar in similars:
                bill_number = similar.get('billnumber')

                if bill_number == second_bill and dup_checker not in dup_checker_list:
                    dup_checker_list.append(dup_checker)
                    dup_checker_list = list(set(dup_checker_list))
                    similar['target_billnumber'] = target_billnumber
                    similar['target_section_header'] = target_section_header
                    similar['target_section_number'] = target_section_number
                    res.append(similar)
        return sorted(res, key=lambda k: k['score'], reverse=True)[:10]

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
    permanent_pdf_link = models.FileField(upload_to='statements/', blank=True, null=True)
    original_pdf_link = models.CharField(max_length=255, null=True, blank=True)
    administration = models.CharField(max_length=100,default='common')

    date_fetched = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.bill_number} - {self.permanent_pdf_link}'


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


class PressStatement(models.Model):
    url = models.CharField(max_length=1000)
    date = models.CharField(max_length=500)
    title = models.TextField()
    statement_type = models.CharField(max_length=500)
    member_id = models.CharField(max_length=500)
    congress = models.CharField(max_length=127)
    member_uri = models.CharField(max_length=1000)
    name = models.CharField(max_length=127, null=True, blank=True)
    chamber = models.CharField(max_length=127, null=True, blank=True)
    state = models.CharField(max_length=127, null=True, blank=True)
    party = models.CharField(max_length=127, null=True, blank=True)
    bill_number = models.CharField(max_length=127)




    def __str__(self):
        return f'{self.congress} {self.bill_number}, {self.url}'

from celery import states

ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))

class PressStatementTask(models.Model):
    congress = models.CharField(max_length = 127)
    bill_number = models.CharField(max_length=127)
    status = models.CharField(
        max_length=50, default=states.PENDING, db_index=True,
        choices=TASK_STATE_CHOICES,
        verbose_name=_('Task State'),
        help_text=_('Current state of the press statement task.')
    )
    task_id = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.congress} {self.bill_number} {self.status}"