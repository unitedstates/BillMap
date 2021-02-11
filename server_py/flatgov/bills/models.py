from collections import Counter
from datetime import datetime
from operator import itemgetter

from django.db import models
from iteration_utilities import flatten, unique_everseen, duplicates

class Bill(models.Model):
    bill_congress_type_number = models.CharField(max_length=100, unique=True, db_index=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    congress = models.IntegerField(null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    titles = models.JSONField(default=list)
    summary = models.TextField(null=True, blank=True)
    titles_whole_bill = models.JSONField(default=list)
    short_title = models.TextField(null=True, blank=True)
    # sponsor = models.ForeignKey(
    #     'bills.Sponsor', on_delete=models.CASCADE, blank=True, null=True)
    sponsor = models.JSONField(default=dict)
    cosponsors = models.ManyToManyField(
        'bills.Cosponsor', blank=True, related_name='cosponsors')
    related_bills = models.JSONField(default=list)
    related_dict = models.JSONField(default=dict)
    cosponsors_dict = models.JSONField(default=list)
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
          'max_item': maxItem 
        })
      return sorted(res, key=lambda k: k['score'], reverse=True)

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
class Cosponsor(models.Model):
    name = models.CharField(max_length=100)
    bioguide_id = models.CharField(max_length=100, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} - {self.name}'

    class Meta:
        unique_together = ('name', 'bioguide_id')


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=300, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    titles = models.JSONField(default=list)
    type = models.CharField(max_length=50, blank=True, null=True)
    thomas_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class BillUpdateJob(models.Model):
    job_id = models.CharField(blank=True, max_length=50, null=True)
    status = models.CharField(choices=[('pending', 'pending'), ('success', 'success')], default='pending', max_length=20)
    content = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
