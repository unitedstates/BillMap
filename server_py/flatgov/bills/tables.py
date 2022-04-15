import itertools
from django.conf import settings

import django_tables2 as tables
from bills.models import Bill


class RelatedBillTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    bill = tables.TemplateColumn(
        '<a href="{% url "bill-detail" record.bill_congress_type_number %}">{{record.bill_congress_type_number}}</a>',
        order_by="bill_congress_type_number"
    )
    reason = tables.Column(empty_values=(), orderable=True)

    class Meta:
        model = Bill
        fields = ['row_number', 'bill', 'reason']
        attrs = settings.DJANGO_TABLES2_STYLE
        sequence = [
            'row_number',
        ]
        empty_text = "There isn't any matched related bills..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.object = args[0]
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    def render_reason(self, record):
        for key, value in self.object.related_dict.items():
            if key == record.bill_congress_type_number:
                return 'identical'
            return value.get('reason')

    def order_reason(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "pk")
        return (queryset, True)
