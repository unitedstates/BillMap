from rest_framework import serializers
from bills.models import Bill


class RelatedBillSerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    cosponsor = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ['bill_congress_type_number', 'reason', 'titles', 'sponsor',
            'cosponsor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bill = self.context.get('bill')

    def get_reason(self, obj):
        if obj == self.bill:
            return 'identical'
        return self.bill.related_dict.get(obj.bill_congress_type_number).get('reason')

    def get_titles(self, obj):
        item = self.bill.related_dict.get(obj.bill_congress_type_number, {})
        if item.get('titles'):
            return ", ".join(item.get('titles'))
        return ""

    def get_sponsor(self, obj):
        if self.bill == obj:
            return obj.sponsor.get('name')
        return ""

    def get_cosponsor(self, obj):
        item = self.bill.related_dict.get(obj.bill_congress_type_number, {})
        if item.get('cosponsors'):
            names = [self.make_name_clean(i.get('name')) \
                for i in item.get('cosponsors')]
            return ", ".join(names)
        return ""

    def make_name_clean(self, name):
        sec = [i.strip() for i in name.split(',')]
        return sec[1] + ' ' + sec[0]
