from django.conf import settings
from django.db.models import Model, CharField, TextField, \
    ManyToManyField, DateField, JSONField


class Bill(Model):
    """
    Bill
    """
    number = CharField(primary_key=True, max_length=16)
    titles = TextField()

    class Meta:
        db_table = 'bill'


class CrsReport(Model):
    """
    CRS report
    """
    title = TextField(help_text='Report title')
    file = TextField(help_text='Report file name')
    bills = ManyToManyField(Bill, help_text='Bills associated with this report')
    date = DateField(help_text='Latest pub date of the report')
    metadata = JSONField(null=True, help_text='Report metadata in JSON form')
    report_content_raw = TextField(
        null=True, help_text='Report raw text extracted from HTML. '
                             'It does not include report summary, look to metadata for it.')

    def get_report_file_path(self):
        return '{}/files/{}'.format(settings.BASE_DIR, self.file)

    class Meta:
        db_table = 'crs_report'

    def __str__(self):
        return '"{}" [{}], {}'.format(self.title, self.date, self.file)
