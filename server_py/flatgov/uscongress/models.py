from celery import current_app
from django.db import models

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
    content = models.JSONField(default=dict)
    fdsys_status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    data_status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    bill_status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    meta_status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    related_status = models.CharField(choices=STATUS, default=PENDING, max_length=20)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.job_id if self.job_id else str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk and self.data_status == self.SUCCESS:
            current_app.send_task(
                'uscongress.tasks.bill_data_task',
                args=(self.pk, ),
                queue='bill'
            )
