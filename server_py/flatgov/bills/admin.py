from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from bills.models import Bill, Sponsor, Cosponsor, BillUpdateJob


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_congress_type_number']
    search_fields = ['bill_congress_type_number']


admin.site.register(Sponsor)
admin.site.register(Cosponsor)
admin.site.register(BillUpdateJob)
