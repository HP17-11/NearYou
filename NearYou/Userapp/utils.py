from django.db.models import Q
from vendor.models import shop
from .models import Customer
from .models import Order

def searchshops(request):
    search_query = ('')

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    shops = shop.objects.distinct().filter(shop_name__icontains=search_query)

    return shops, search_query


