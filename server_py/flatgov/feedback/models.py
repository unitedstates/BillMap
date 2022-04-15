from django.db import models
from rest_framework.reverse import reverse


class Feedback(models.Model):
    is_helpful = models.BooleanField()
    content = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.is_helpful} {self.created_at}'

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
