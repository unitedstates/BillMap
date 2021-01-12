from django.urls import path

from . import views

urlpatterns = [
    path('', views.UscongressTestView, name='uscongress-test'),
]
