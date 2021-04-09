from rest_framework import serializers
from bills.models import Bill, Cosponsor


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


class CosponsorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    bills = serializers.SerializerMethodField()

    class Meta:
        model = Cosponsor
        fields = ['name', 'bills', 'party']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bill = self.context.get('bill')

    def get_party(self, obj):
        return obj.party

    def get_name(self, obj):
        return obj.name_full_official

    def get_bills(self, obj):
        bills = self.bill.get_cosponsor_bill(obj.name)
        if not bills:
            return self.bill.bill_congress_type_number
        return self.bill.bill_congress_type_number + ', ' + ', '.join(bills)

    def make_name_clean(self, name):
        sec = [i.strip() for i in name.split(',')]
        return sec[1] + ' ' + sec[0]


class BillNumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_congress_type_number']
