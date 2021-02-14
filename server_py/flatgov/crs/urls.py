from django.urls import path
from crs.views import csv_report

urlpatterns = [
    path('csv-report/', csv_report),
]
