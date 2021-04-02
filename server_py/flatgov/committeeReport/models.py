from django.db import models

class CommitteeReportScrapyTask(models.Model):
    congress = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        pk = str(self.pk)
        congress = str(self.congress)
        return f"{pk} - {congress}"
