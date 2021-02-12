import csv
from django.http import HttpResponse
from crs.models import CrsReport


def csv_report(request):
    report_content = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=crs_reports.csv'
    writer = csv.writer(response)
    writer.writerow(['Report ID', 'Bill #', 'Report title', 'Report file path',
                     'Report date', 'Has metadata', 'Has report content'])
    for report in CrsReport.objects.all():
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
