from django.contrib import admin

from home.models import (
    AboutPage
)


class AboutPageAdmin(admin.ModelAdmin):
    class Meta:
        model = AboutPage

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


admin.site.register(AboutPage, AboutPageAdmin)
