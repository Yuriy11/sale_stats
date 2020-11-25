from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CurrencyRatioToUAHAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'code', 'ratio')
    list_display_links = ('pk',)
    list_editable = ('date', 'code', 'ratio')


class DailySaleResultsResource(resources.ModelResource):
    class Meta:
        model = DailySaleResultsByUTM


class DailySaleResultsByUTMAdmin(ImportExportModelAdmin):
    resource_class = DailySaleResultsResource
    list_display = ('pk', 'date', 'UTM', 'requests', 'orders', 'in_new_status','in_cant_reach_status','in_not_ordered_status','in_refused_status','ratio_approve','ratio_new','ration_cant_reach','ration_not_ordered','ratio_refused','revenue','average_purchase_value_UAH','currency_ratio_to_UAH')
    list_display_links = ('pk',)
    list_editable = ('date', 'UTM', 'requests', 'orders', 'in_new_status','in_cant_reach_status','in_not_ordered_status','in_refused_status','ratio_approve','ratio_new','ration_cant_reach','ration_not_ordered','ratio_refused','revenue','average_purchase_value_UAH')


admin.site.register(DailySaleResultsByUTM, DailySaleResultsByUTMAdmin)
admin.site.register(CurrencyRatioToUAH, CurrencyRatioToUAHAdmin)
# Register your models here.
