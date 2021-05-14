from django.urls import path
from crs.views import csv_report, CSVDownloadView

urlpatterns = [
    path('csv-report/', CSVDownloadView.as_view(), name='csv-download'),
]
