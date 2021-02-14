from django.conf import settings
from django.db import models
from bills.models import Bill


class CrsReport(models.Model):
    """
    CRS report
    """
    title = models.TextField(help_text='Report title')
    file = models.TextField(help_text='Report file name')
    bills = models.ManyToManyField(Bill, help_text='Bills associated with this report')
    date = models.DateField(help_text='Latest pub date of the report')
    metadata = models.JSONField(null=True, help_text='Report metadata in JSON form')
    report_content_raw = models.TextField(
        null=True, help_text='Report raw text extracted from HTML. '
                             'It does not include report summary, look to metadata for it.')

    def get_report_file_path(self):
        return '{}/files/{}'.format(settings.BASE_DIR, self.file)

    class Meta:
        db_table = 'crs_report'

    def __str__(self):
        return '"{}" [{}], {}'.format(self.title, self.date, self.file)
