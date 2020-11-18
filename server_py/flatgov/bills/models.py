from django.db import models

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
    cosponsors_dict = models.JSONField(default=list)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bill_congress_type_number

    def get_type_abbrev(self) -> str:
        return ''.join([letter.upper() + '.' for letter in self.type])

    def get_related_bill_numbers(self):
        return [bill.get('billCongressTypeNumber') for bill in self.related_bills]


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
