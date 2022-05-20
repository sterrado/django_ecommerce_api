from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.Product.as_view(), name='products_list'),
    path('products/<int:product_id>/',
         views.Product.as_view(), name='products_process'),
    path('orders/', views.Order.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', views.Order.as_view(), name='orders_process'),
]
