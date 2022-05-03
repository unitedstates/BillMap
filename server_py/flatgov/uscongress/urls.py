from django.urls import path

from uscongress import views

urlpatterns = [
    path('', views.UscongressDebugView.as_view(), name='uscongress-test'),
]
