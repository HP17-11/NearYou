from django.db.models import Q
from LocalMarket.models import Product, Order
from .models import shop
from LocalMarket.forms import Cart_shopview

def searchproducts(request, pk):

    search_query = ('')

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    # products = Product.objects.filter(shop_id=pk)
    products = Product.objects.distinct().filter(product_name__icontains=search_query, shop_id=pk)

    return products, search_query

def finaltotal(request, pk):

    shops = shop.objects.filter(vendor_id=pk)
    orders_all = []
    for shop_i in shops:
        orders = Order.objects.filter(shop_id=shop_i.shop_id)
        orders_all.append(orders)
    order_data = []
    total_final_amount = 0
    for i in range(len(orders_all)):
        for order in orders_all[i]:
            order_items_count = order.orderitem_set.all().count()
            orderitems = order.orderitem_set.all()
            sum = 0
            for orderitem in orderitems:
                sum = sum + float(orderitem.amount)
            print(sum)
            order.total_amount = str(sum)
            del_amount = 5
            tax_amount = round(float(order.total_amount) * 1.13, 2)
            print(tax_amount)
            final_amount = del_amount + tax_amount
            total_final_amount = total_final_amount + final_amount
            print(order.total_amount)
            print(final_amount)
            order.save()
            order_data.append({'order': order, 'order_items_count': order_items_count, 'total_amount': final_amount})

    return order_data, final_amount, total_final_amount

#
# def editproduct(request, pk):
#
#     product = Product.objects.get(product_id=pk)
#     form = Cart_shopview(instance=product)
#
#     if request.method == 'POST':
#         form = Cart_shopview(request.POST, instance=product)
#         if form.is_valid():
#             form.save()

