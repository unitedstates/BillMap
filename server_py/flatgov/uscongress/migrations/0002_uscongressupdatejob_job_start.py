# Generated by Django 3.1.12 on 2021-08-31 15:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('uscongress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uscongressupdatejob',
            name='job_start',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
