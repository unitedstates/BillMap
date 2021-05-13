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

    row = ['Report ID', 'Bill #', 'Report title', 'Report file path',
                     'Report date', 'Has metadata', 'Has report content']
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
            
    for report in CrsReport.objects.all().iterator():
        for bill in report.bills.all().iterator():
            csv_writer.writerow([
                report.pk,
                bill.number,
                report.title,
                report.get_report_file_path(),
                report.date,
                report.metadata is not None,
                report.report_content_raw != ''
            ])
    content_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
    csv_report.file.save('crs_reports.csv', content_file)
    

