from collections import Counter
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
    related_dict = models.JSONField(default=dict)
    cosponsors_dict = models.JSONField(default=list)
    es_similarity = models.JSONField(default=list)

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
        section_obj = dict()

        es_similarity = self.es_similarity
        for section in es_similarity:
            similars = section.get('similars')
            section_num = section.get('section_number')
            section_header = section.get('section_header')

            for similar in similars:
                billnumber = similar.get('billnumber')
                score = similar.get('score')
                title = similar.get('title')

                target = section_obj.get(billnumber, {})
                title_list = target.get('title', [])
                title_list.append(title)

                scores_list = target.get('scores', [])
                scores_list.append({
                    'score': score,
                    'section_num': section_num,
                    'section_header': section_header,
                })
                sorted_scores_list = sorted(scores_list, key=lambda k: k['score'], reverse=True)

                target['score'] = target.get('score', 0) + score
                target['title'] = title_list
                target['number_of_sections'] = target.get('number_of_sections', 0) + 1
                target['scores'] = sorted_scores_list
                section_obj[billnumber] = target
                # score = similar.get('score')
                # billnumber = similar.get('billnumber')
                # res[billnumber] += score

        for bill_congress_type_number, obj in section_obj.items():
            qs_bill = Bill.objects.filter(
                bill_congress_type_number=bill_congress_type_number)
            score = obj.get('score')
            if qs_bill.exists():
                in_db = True
            else:
                in_db = False

            res.append({
                "score": score,
                "in_db": in_db,
                "bill_congress_type_number": bill_congress_type_number,
                "info": obj
            })
        return sorted(res, key=lambda k: k['score'], reverse=True)

    def get_second_similar_bills(self, second_bill):
        res = list()
        target_section_header_list = list()

        for item in self.es_similarity:
            similars = item.get('similars')
            target_billnumber = item.get('billnumber')
            target_section_header = item.get('section_header')
            target_section_number = item.get('section_number')

            if not similars:
                continue

            if target_section_header in target_section_header_list:
                continue
            else:
                target_section_header_list.append(target_section_header)

            for similar in similars:
                bill_number = similar.get('billnumber')

                if bill_number == second_bill:
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
