from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home_view, name='home'),
]

api_urlpatterns = [
    path('bill-list/', views.BillListAPIView.as_view(), name='bill-list'),
]

urlpatterns += api_urlpatterns
