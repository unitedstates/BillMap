# Generated by Django 3.1 on 2021-01-12 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uscongress', '0007_auto_20210112_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uscongressupdatejob',
            old_name='skipped',
            new_name='skips',
        ),
    ]