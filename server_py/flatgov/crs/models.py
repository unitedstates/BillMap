from celery import current_app

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

    meta_url = models.URLField()
    html_url = models.URLField()

    def get_report_file_path(self):
        return '{}/files/{}'.format(settings.BASE_DIR, self.file)

    class Meta:
        db_table = 'crs_report'

    def __str__(self):
        return '"{}" [{}], {}'.format(self.title, self.date, self.file)


class CSVReport(models.Model):
    task_id = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(upload_to='crs/', null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = False
        if not self.pk:
            created = True
        super().save(*args, **kwargs)
        if created:
            current_app.send_task(
                'crs.tasks.generate_csv_task',
                args=(self.pk, ),
                queue='bill'
            )

    def delete(self, using=None, keep_parents=False):
        """
        keep parents while deleting the contact list.
        """
        self.file.delete(save=False)
        super().delete(using, keep_parents)
