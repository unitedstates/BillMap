"""flatgov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url='home/', permanent=False), name='index'),
    path('bills/', include('bills.urls')),
    path('home/', include('home.urls')),
    path('uscongress/debug/', include('uscongress.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

