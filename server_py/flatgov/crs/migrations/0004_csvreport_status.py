# Generated by Django 3.1.8 on 2021-05-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crs', '0003_auto_20210513_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvreport',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
