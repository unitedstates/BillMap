import csv
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from crs.models import CSVReport, CrsReport


def csv_report(request):
    report_content = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=crs_reports.csv'
    writer = csv.writer(response)
    writer.writerow(['Report ID', 'Bill #', 'Report title', 'Report file path',
                     'Report date', 'Has metadata', 'Has report content'])
    for report in CrsReport.objects.all().iterator():
        for bill in report.bills.all():
            report_content.append([
                report.pk,
                bill.number,
                report.title,
                report.get_report_file_path(),
                report.date,
                report.metadata is not None,
                report.report_content_raw != ''
            ])
    writer.writerows(report_content)
    return response


class CSVDownloadView(TemplateView):
    template_name = 'CRSDownload.html'

    def post(self, request, *args, **kwargs):
        report = CSVReport.objects.first()
        if report:
            report.delete()

        report = CSVReport.objects.create()

        messages.success(request, 'Please wait for a while...')
        return render(request, self.template_name, {'file': report})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = CSVReport.objects.first()
        return context
