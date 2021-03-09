from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from bills.models import Bill, Sponsor, Cosponsor, Statement, CboReport, CommitteeDocument
from crs.models import CrsReport 


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_congress_type_number']
    search_fields = ['bill_congress_type_number']


admin.site.register(Sponsor)
admin.site.register(Cosponsor)
admin.site.register(Statement)
admin.site.register(CrsReport)
admin.site.register(CboReport)
admin.site.register(CommitteeDocument)

