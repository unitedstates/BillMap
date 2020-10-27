from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'similar', views.similar_bills_view),
    path('<str:bill>', views.bill_view)

]