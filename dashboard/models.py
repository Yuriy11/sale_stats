from django.db import models
import django_filters
from django.db.models.signals import pre_save
import requests
from datetime import timedelta
from datetime import date


class CurrencyRatioToUAH(models.Model):
    code = models.CharField(max_length=3)
    ratio = models.FloatField()
    date = models.DateField()


class DailySaleResultsByUTM(models.Model):
    date = models.DateField()
    UTM = models.CharField(max_length=400)
    requests = models.IntegerField()
    orders = models.IntegerField()
    in_new_status = models.IntegerField()
    in_cant_reach_status = models.IntegerField()
    in_not_ordered_status = models.IntegerField()
    in_refused_status = models.IntegerField()
    ratio_approve = models.FloatField()
    ratio_new = models.FloatField()
    ration_cant_reach = models.FloatField()
    ration_not_ordered = models.FloatField()
    ratio_refused = models.FloatField()
    revenue = models.FloatField()
    average_purchase_value_UAH = models.FloatField()
    currency_ratio_to_UAH = models.ForeignKey(to=CurrencyRatioToUAH, on_delete=models.SET_NULL, null=True, blank=True)

    # add average return rate
    def save(self, *args, **kwargs):
        add_missing_currency_ratios('USD')
        self.currency_ratio_to_UAH = CurrencyRatioToUAH.objects.filter(code__exact='USD', date__exact=self.date)[0]
        super(DailySaleResultsByUTM, self).save(*args, **kwargs)


class DailySaleResultsByUTMFilter(django_filters.FilterSet):
    class Meta:
        model = DailySaleResultsByUTM
        fields = ['date', 'UTM', 'requests', 'orders', 'in_new_status', 'in_cant_reach_status', 'in_not_ordered_status',
                  'in_refused_status', 'ratio_approve', 'ratio_new', 'ration_cant_reach', 'ration_not_ordered',
                  'ratio_refused', 'revenue', 'average_purchase_value_UAH']


###################LOGIC
###################LOGIC
###################LOGIC
###################LOGIC


def write_currency_ratio_for_date(currency, input_date):
    query = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + str(input_date.day) + '.' + str(
        input_date.month) + '.' + str(input_date.year)
    session = requests.Session()
    df = session.get(query)
    response = df.json()
    response['exchangeRate'][0]['currency'] = 1
    for i in response['exchangeRate']:
        if i['currency'] == currency:
            result = i['purchaseRateNB']
            break;
    CurrencyRatioToUAH.objects.create(code=currency, date=input_date, ratio=result).save()


def add_missing_currency_ratios(currency):
    today = date.today()
    last_retrieved = CurrencyRatioToUAH.objects.order_by('-date')[0].date
    last_retrieved += timedelta(days=1)
    while today >= last_retrieved:
        write_currency_ratio_for_date(currency, last_retrieved)
        last_retrieved += timedelta(days=1)
