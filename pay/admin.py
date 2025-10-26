from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User 

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# Order Item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem 
    extra = 0
    
# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = OrderItem
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped", "phone_number", "paid"]
    inlines = [OrderItemInline]
    
    
# Unregister order Model
admin.site.unregister(Order)

# Re-register our order and orderAdmin
admin.site.register(Order, OrderAdmin)
    
    
    
    
