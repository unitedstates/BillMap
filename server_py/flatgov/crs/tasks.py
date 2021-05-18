import csv
from io import StringIO
from celery import shared_task

from django.core.files.base import ContentFile

from crs.models import CSVReport, CrsReport

@shared_task(bind=True)
def generate_csv_task(self, pk):
    csv_report = CSVReport.objects.get(pk=pk)
    csv_report.task_id = self.request.id
    csv_report.save(update_fields=['task_id'])

    try:
        header_row = ['Bill #', 'Report Date', 'Report Title',
                        'Report Metadata url', 'Report HTML url']
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(header_row)
                
        for report in CrsReport.objects.all().iterator():
            for bill in report.bills.all().iterator():
                csv_writer.writerow([
                    bill.bill_congress_type_number,
                    report.date,
                    report.title,
                    report.meta_url,
                    report.html_url
                ])
        content_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
        csv_report.file.save('crs_reports.csv', content_file)
    except Exception as e:
        csv_report.log = e
        csv_report.save(update_fields=['log'])
