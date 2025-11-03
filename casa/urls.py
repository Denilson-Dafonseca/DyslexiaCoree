from django.urls import path
from . import views 


urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('stand/', views.stand, name='stand'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:bk>', views.category, name='category'),
    path('register/', views.register_user, name='register'),
    path('door_to_door_relief/', views.door_to_door_relief, name='door_to_door_relief'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('search/', views.search, name='search'),
    path('info/', views.info, name='info'),
    path('payment_method/', views.payment_method, name='payment_method'),
]