from . import models
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist
import requests

# Create your views here.


class Product(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, product_id=0):
        if (product_id > 0):
            products = list(models.Product.objects.filter(
                product_id=product_id).values())
            if len(products) > 0:
                product = products[0]
                datos = {'message': "Success", 'product': product}
            else:
                datos = {'message': "product not found..."}
            return JsonResponse(datos)
        else:
            products = list(models.Product.objects.values())
            if len(products) > 0:
                datos = {'message': "Success", 'products': products}
            else:
                datos = {'message': "products not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        models.Product.objects.create(
            product_id=jd['product_id'], name=jd['name'], stock=jd['stock'], price=jd['price'])
        datos = {'message': "Success"}
        return JsonResponse(datos)

    def put(self, request, product_id):
        jd = json.loads(request.body)
        products = list(models.Product.objects.filter(
            product_id=product_id).values())
        if len(products) > 0:
            product = models.Product.objects.get(product_id=product_id)
            product.name = jd['name']
            product.price = jd['price']
            product.stock = jd['stock']
            product.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Product not found..."}
        return JsonResponse(datos)

    def delete(self, request, product_id):
        product = list(models.Product.objects.filter(
            product_id=product_id).values())
        if len(product) > 0:
            models.Product.objects.filter(product_id=product_id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Product not found..."}
        return JsonResponse(datos)


class Order(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id=0):
        if (order_id > 0):
            orders = list(models.Order.objects.filter(
                order_id=order_id).values())
            if len(orders) > 0:
                order = orders[0]
                datos = {'message': "Success", 'order': order}
            else:
                datos = {'message': "order not found..."}
            return JsonResponse(datos)
        else:
            orders = list(models.Order.objects.values())
            if len(orders) > 0:
                datos = {'message': "Success", 'orders': orders}
            else:
                datos = {'message': "orders not found..."}
            return JsonResponse(datos)

    def get_total(self, request, order_id):
        orders = list(models.Order.objects.filter(order_id=order_id).values())
        if len(orders) > 0:
            order = orders[0]
            product = models.Product.objects.get(product_id=order.product_id)
            return JsonResponse({'total': product.price * order.order_quantity})
        else:
            return JsonResponse({'message': 'order not found...'})

    def get_total_usd(self, request, order_id):
        orders = list(models.Order.objects.filter(order_id=order_id).values())
        r = requests.get(
            'https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
        r = r.text
        for dict in r:
            dict = dict['casa']
            if dict['nombre'] == 'Dolar Blue':
                valor_dolar = dict['venta']
        if len(orders) > 0:
            order = orders[0]
            product = models.Product.objects.get(product_id=order.product_id)
            return JsonResponse({'total': product.price * valor_dolar * order.order_quantity})
        else:
            return JsonResponse({'message': 'order not found...'})

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        product = models.Product.objects.get(product_id=jd['product'])
        product.stock = product.stock - jd['order_quantity']
        product.save()
        models.Order.objects.create(
            order_id=jd['order_id'], order_quantity=jd['order_quantity'],  product_id=jd['product'])
        datos = {'message': "Success"}
        return JsonResponse(datos)

    def put(self, request, order_id):
        jd = json.loads(request.body)
        orders = list(models.Order.objects.filter(order_id=order_id).values())
        if len(orders) > 0:
            order = models.Order.objects.get(order_id=order_id)
            product = models.Product.objects.get(product_id=jd['product'])
            product.stock = product.stock - \
                jd['order_quantity'] + order.order_quantity
            product.save()
            order.product_id = jd['product']
            order.order_quantity = jd['order_quantity']
            order.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "order not found..."}
        return JsonResponse(datos)

    def delete(self, request, order_id):
        order = list(models.Order.objects.filter(order_id=order_id).values())
        if len(order) > 0:
            order = models.Order.objects.get(order_id=order_id)
            product = models.Product.objects.get(
                product_id=order.product_id)
            product.stock = product.stock + order.order_quantity
            product.save()
            models.Order.objects.filter(order_id=order_id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "order not found..."}
        return JsonResponse(datos)


"""
@api_view()
def say_hello(request):
    return Response('Hello')


@api_view()
def register_or_update_product(request, product: models.Product):
    query_set = models.Product.objects.exists(pk=product.product_id)
    return Response(query_set)


@api_view()
def delete_product(request, id):
    pass


@api_view()
def get_product(request, id):
    try:
        product = models.Product.objects.get(pk=id)
    except ObjectDoesNotExist:
        pass


@api_view()
def get_all_products():
    pass


@api_view()
def update_stock(request):
    pass


@api_view()
def register_or_update_order(request: models.Order):
    pass


@api_view()
def delete_order(request, id):
    pass


@api_view()
def get_order(request, id):
    pass


@api_view()
def get_all_orders():
    pass
"""
