from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta

from .models import Company
from stock.models import Stock
from company.dto import Company_DTO

def index(request):
    sort_attr = request.GET.get('sort', 'name')
    NUM_DAYS = 365
    objList = Company.objects.order_by("name")
    dto_list = []
    latest_date = Stock.objects.order_by("-record_date").first().record_date
    for company in objList:
        dto = {}
        dto['name'] = company.name
        dto['valid'] = False
        stocks = Stock.objects.filter(company__id=company.id).order_by("-record_date").filter(record_date__gte=datetime.now()-timedelta(days=NUM_DAYS)).all()
        if stocks and len(stocks) > 0:
            latest_stock = stocks[0]
            if latest_date == latest_stock.record_date:
                dto['close'] = latest_stock.close
                dto['valid'] = True
                max_close=float('-inf')
                min_close=float('inf')
                for stock in stocks:
                    if stock.close > max_close:
                        max_close = stock.close
                    if stock.close < min_close:
                        min_close = stock.close
                dto['min_close'] = min_close
                dto['max_close'] = max_close
                dto['min_percent'] = round((dto['close'] - dto['min_close'])/dto['close'] * 100, 2)
                dto['max_percent'] = round((dto['max_close'] - dto['close'])/dto['close'] * 100, 2)
            else:
                print("Latest Date should be {}, but is: {} for {}".format(latest_date, latest_stock.record_date, company.name))
        dto_list.append(dto)
            
    context = {'table': Company_DTO(dto_list), 'date': latest_date}
    context['table'].order_by = sort_attr
    return render(request, 'company/index.html', context)

def detail(request, company_id):
    objList = Stock.objects.filter(company__id=company_id).order_by("-record_date").filter(record_date__gte=datetime.now()-timedelta(days=365)).all()
    context = {'stocks_data': objList}
    return render(request, 'company/stock_listing.html', context)

