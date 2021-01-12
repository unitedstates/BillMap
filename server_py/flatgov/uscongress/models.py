from django.db import models

class UscongressUpdateJob(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    STATUS = (
        (PENDING, PENDING),
        (SUCCESS, SUCCESS),
    )

    job_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    content = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.job_id if self.job_id else self.status
