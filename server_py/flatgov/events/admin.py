from django.contrib import admin
from events.models import Event, SourceArchive

# Register your models here.
admin.site.register(Event)
admin.site.register(SourceArchive)
