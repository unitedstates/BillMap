from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from bills.models import Bill, Committee, Cosponsor, Statement, CboReport, CommitteeDocument
from crs.models import CrsReport, CSVReport


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_congress_type_number']
    search_fields = ['bill_congress_type_number']


admin.site.register(Committee)
admin.site.register(Cosponsor)
admin.site.register(Statement)
admin.site.register(CboReport)
admin.site.register(CommitteeDocument)
admin.site.register(CSVReport)

@admin.register(CrsReport)
class CrsReportAdmin(admin.ModelAdmin):
    """Admin field for CrsReport model."""
    autocomplete_fields = ['bills']
