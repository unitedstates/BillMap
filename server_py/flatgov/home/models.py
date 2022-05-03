from ckeditor.fields import RichTextField
from django.db import models


class AboutPage(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True, default='About page content')
    content = RichTextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} updated on {self.updated_at}'
