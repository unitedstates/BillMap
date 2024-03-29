# Generated by Django 3.1.12 on 2021-08-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sourceName', models.CharField(blank=True, max_length=100, null=True)),
                ('sourceId', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('className', models.CharField(blank=True, max_length=500, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('startTime', models.CharField(blank=True, max_length=20, null=True)),
                ('endTime', models.CharField(blank=True, max_length=20, null=True)),
                ('startRecur', models.DateTimeField(blank=True, null=True)),
                ('endRecur', models.DateTimeField(blank=True, null=True)),
                ('allDay', models.BooleanField(blank=True, null=True)),
                ('daysOfWeek', models.JSONField(default=list)),
                ('eventId', models.CharField(blank=True, max_length=100, null=True)),
                ('referenceUrl', models.CharField(blank=True, max_length=5000, null=True)),
                ('url', models.CharField(blank=True, max_length=5000, null=True)),
                ('chamber', models.CharField(blank=True, max_length=100, null=True)),
                ('committeeCode', models.CharField(blank=True, max_length=100, null=True)),
                ('committee', models.CharField(blank=True, max_length=200, null=True)),
                ('subcommittee', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceArchive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=5000, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.TextField(blank=True, choices=[('downloading', 'downloading'), ('success', 'success'), ('failed', 'failed')], default='downloading', max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
