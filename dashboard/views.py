from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from .models import *


def index():
    return HttpResponse("test")


def stats_list(request):
    f = DailySaleResultsByUTMFilter(request.GET, queryset=DailySaleResultsByUTM.objects.all())
    return render(request, 'dashboard/dashboard.html', {'filter': f})


def stats_list_utm(request):
    f = DailySaleResultsByUTMFilter(request.GET,
                               queryset=DailySaleResultsByUTM.objects.values('UTM').annotate(Sum('orders'), Sum('refuses'),
                                                                                             Sum('items_sold')))
    return render(request, 'dashboard/dashboard_utm.html', {'filter': f})


def stats_list_site(request):
    f = DailySaleResultsByUTMFilter(request.GET,
                               queryset=DailySaleResultsByUTM.objects.values('page_link').annotate(Sum('orders'),
                                                                                                   Sum('refuses'),
                                                                                                   Sum('items_sold')))
    return render(request, 'dashboard/dashboard_link.html', {'filter': f})
