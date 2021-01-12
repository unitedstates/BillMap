from django.urls import path

from . import views

urlpatterns = [
    path('', views.UscongressDebugView.as_view(), name='uscongress-test'),
]
