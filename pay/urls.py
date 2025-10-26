from django.urls import path, include
from . import views 


urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('paid_dash/', views.paid_dash, name='paid_dash'),
    path('not_paid_dash/', views.not_paid_dash, name='not_paid_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
]