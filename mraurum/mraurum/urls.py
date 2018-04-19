"""mraurum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from jmms import views

urlpatterns = [
    url(r'^$', views.index, name='sitehome'),
    url(r'^index/', views.index, name='sitehome'),
    url(r'^jet/', include('jet.urls','jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^trackjewellery/', views.get_jewellery_in_progress, name='progress'),
    url(r'^charts/', views.get_charts, name='charts'),
    url(r'^stock/', views.get_stock, name='stock'),
    url(r'^users/cutter/', views.get_cutters, name='cutters'),
    url(r'^users/embedder/', views.get_embedders, name='embedders'),
    url(r'^users/polisher/', views.get_polishers, name='polishers'),
    url(r'^users/supplier/', views.get_suppliers, name='suppliers'),
    url(r'^users/sellers/', views.get_sellers, name='sellers'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()