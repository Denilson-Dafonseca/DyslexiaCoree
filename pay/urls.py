from django.urls import path, include
from . import views 


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paid_dash/', views.paid_dash, name='paid_dash'),
    path('not_paid_dash/', views.not_paid_dash, name='not_paid_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('order_placed/', views.order_placed, name='order_placed'),
]