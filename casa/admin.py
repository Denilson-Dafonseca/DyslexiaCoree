
from django.contrib import admin
from .models import Product, Category, Customer, CarouselSlide, Profile, Relief, Video, VehicleRequest 
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(CarouselSlide)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Relief)
admin.site.register(Video)
admin.site.register(VehicleRequest)
 
class ProfileInline(admin.StackedInline):
      model = Profile
        
class UserAdmin(admin.ModelAdmin):
      model = User
      field = ["username", "first_name", "last_name", "email"]
      inlines = [ProfileInline]
      

admin.site.unregister(User)     

admin.site.register(User,UserAdmin) 

      

      

