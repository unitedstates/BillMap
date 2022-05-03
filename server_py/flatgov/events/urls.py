from django.urls import path

from events import views

urlpatterns = [
    path('', views.get_events),
    path('committees', views.get_committees)
]
