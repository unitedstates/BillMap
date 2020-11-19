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

    def get_reason(self, obj):
        bill = self.context.get('bill')
        if obj == bill:
            return 'identical'
        return bill.related_dict.get(obj.bill_congress_type_number).get('reason')

    def get_titles(self, obj):
        if obj.titles:
            return ", ".join(obj.titles)
        return ""

    def get_sponsor(self, obj):
        return obj.sponsor.get('name')

    def get_cosponsor(self, obj):
        return ", ".join(obj.cosponsors.values_list('name', flat=True))
