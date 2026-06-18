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
    path('advert/', views.advert, name='advert'),
    path('Affiliate/', views.Affiliate, name="Affiliate"),
    path('Credit/', views.Credit, name="Credit"),
    path('Vendor/', views.Vendor, name="Vendor"),
    path('Purchasing_steps/', views.Purchasing_steps, name="Purchasing_steps"),
    path('Privacy_Policy/', views.Privacy_Policy, name="Privacy_Policy"),
    path('Terms_of_service/', views.Terms_of_service, name="Terms_of_service"),
    path('Car_order/', views.Car_order, name="Car_order"),
    path('done/<int:id>/', views.mark_done, name='mark_done'),
    path('Not_secured/', views.Not_secured, name="Not_secured"),
    path('Secured_deal/', views.Secured_deal, name="Secured_deal"),
    path('clothing', views.clothing_order, name='clothing_order'),
    
]