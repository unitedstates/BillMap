from django.apps import AppConfig
from django.db.models.signals import post_migrate


class FlatGovConfig(AppConfig):
    name = 'FlatGov'
    verbose_name = 'FlatGov'

    def ready(self):
        from FlatGov.bills_import import bills_to_db
        post_migrate.connect(bills_to_db, sender=self)
