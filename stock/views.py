from django.http import HttpResponse

from .models import Stock

def index(request):
    objList = Stock.objects.order_by('date')
    return HttpResponse(objList)