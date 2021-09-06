from django.urls import path
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache

from . import views
from .propublica_api_views import GetPressStatementsAPIView

app_name = 'home'

urlpatterns = [
    # path('', views.index, name='index'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('home/', views.home_view, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
]

api_urlpatterns = [
    path('home/bill-list/', never_cache(views.BillListAPIView.as_view()), name='bill-list'),
    path('home/bill-titles/<congressnumber>', never_cache(views.BillListTitleAPIView.as_view()), name='bill-titles'),
    path('home/bill-title/<bill>/', never_cache(views.GetBillTitleAPIView.as_view()), name='bill-title'),
    path('press-statements/<congress>/<bill_type>/<bill_number>/', never_cache(GetPressStatementsAPIView.as_view()), name='press-statements'),
]

urlpatterns += api_urlpatterns
