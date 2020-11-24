from django.urls import path

from . import views

urlpatterns = [
    path('', views.BillListView.as_view(), name='bill-list'),
    path(r'similar', views.similar_bills_view),
    # path('<str:bill>', views.bill_view),
    path('<str:slug>', \
        views.BillDetailView.as_view(), name='bill-detail')

]