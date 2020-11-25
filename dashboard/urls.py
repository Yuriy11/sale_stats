from django.urls import path
from django.conf.urls import url
from django_filters.views import FilterView
from .models import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^list$', views.stats_list),
    url(r'^list/utm$', views.stats_list_utm),
    url(r'^list/site$', views.stats_list_site)
]
