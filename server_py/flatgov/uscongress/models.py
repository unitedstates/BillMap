from celery import current_app
from django.db import models
from datetime import datetime


class UscongressUpdateJob(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS = (
        (PENDING, PENDING),
        (SUCCESS, SUCCESS),
        (FAILED, FAILED),
    )

    job_id = models.CharField(max_length=50, blank=True, null=True)
    job_start = models.DateTimeField(auto_now_add=True)
    fdsys_status = models.CharField(choices=STATUS,
                                    default=PENDING,
                                    max_length=20)
    data_status = models.CharField(choices=STATUS,
                                   default=PENDING,
                                   max_length=20)
    bill_status = models.CharField(choices=STATUS,
                                   default=PENDING,
                                   max_length=20)
    meta_status = models.CharField(choices=STATUS,
                                   default=PENDING,
                                   max_length=20)
    related_status = models.CharField(choices=STATUS,
                                      default=PENDING,
                                      max_length=20)
    elastic_status = models.CharField(choices=STATUS,
                                      default=PENDING,
                                      max_length=20)
    similarity_status = models.CharField(choices=STATUS,
                                         default=PENDING,
                                         max_length=20)

    saved = models.JSONField(default=list, blank=True, null=True)
    skips = models.JSONField(default=list, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.job_id if self.job_id else str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk and self.data_status == self.SUCCESS and self.bill_status == self.PENDING:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}:  {self.job_id}: bill_status = SUCCESS; starting bill_data_task')
            current_app.send_task('uscongress.tasks.bill_data_task',
                                  args=(self.pk, ),
                                  queue='bill')
        if self.pk and self.bill_status == self.SUCCESS and self.meta_status == self.PENDING:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}:  {self.job_id}: bill_status = SUCCESS; starting bill_meta_task')
            current_app.send_task('uscongress.tasks.process_bill_meta_task',
                                  args=(self.pk, ),
                                  queue='bill')

        if self.pk and self.meta_status == self.SUCCESS and self.related_status == self.PENDING:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}:  {self.job_id}: meta_status = SUCCESS; starting related_bill_task')
            current_app.send_task('uscongress.tasks.related_bill_task',
                                  args=(self.pk, ),
                                  queue='bill')

        if self.pk and self.related_status == self.SUCCESS and self.elastic_status == self.PENDING:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}:  {self.job_id}: related_status = SUCCESS; starting elastic_load_task')
            current_app.send_task('uscongress.tasks.elastic_load_task',
                                  args=(self.pk, ),
                                  queue='bill')

        if self.pk and self.elastic_status == self.SUCCESS and self.similarity_status == self.PENDING:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}:  {self.job_id}: elastic_status = SUCCESS; starting bill_similarity_task')
            current_app.send_task('uscongress.tasks.bill_similarity_task',
                                  args=(self.pk, ),
                                  queue='bill')

    @property
    def get_saved_bill_list(self):
        res = list()
        saved = self.data_content.get('saved')
        if not saved:
            return list()
        for bill in saved:
            bill_id, congress = bill.split('-')[1], bill.split('-')[0]
            res.append(f'{congress}{bill_id}')
        return res
