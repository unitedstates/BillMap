from django.db import models

class Bill(models.Model):
    bill_congress_type_number = models.CharField(max_length=100, unique=True)
    title = models.JSONField(default=list)
    titles_whole_bill = models.JSONField(default=list)

    cosponsors = models.ManyToManyField(
        'bills.Sponsor', blank=True, related_name='cosponsors')
    related_bills = models.ManyToManyField('self', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bill_congress_type_number


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    bioguide_id = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return bioguide_id
