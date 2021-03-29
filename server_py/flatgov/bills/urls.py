from django.urls import path
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', never_cache(views.BillListView.as_view()), name='bill-list'),
    path(r'similar', views.similar_bills_view),
    # path('<str:bill>', views.bill_view),
    path('<str:slug>', \
        never_cache(views.BillDetailView.as_view()), name='bill-detail'),
    path('compare/<str:slug>/<str:second_bill>/', \
        never_cache(views.BillToBillView.as_view()), name='bill-to-bill'),
]