from django.urls import path
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('', views.home_view, name='home'),
]

api_urlpatterns = [
    path('bill-list/', never_cache(views.BillListAPIView.as_view()), name='bill-list'),
]

urlpatterns += api_urlpatterns
