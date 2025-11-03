from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'email',
        'amount_paid',
        'payment_method',
        'payment_reference',
        'paid',
        'shipped',
        'date_ordered',
        'date_paid',
        'date_shipped',
    ]

    list_filter = [
        'paid',
        'shipped',
        'payment_method',
        'date_ordered',
        'date_paid',
        'date_shipped',
    ]

    search_fields = [
        'full_name',
        'email',
        'payment_reference',
        'payment_method',
        'shipping_address',
    ]

    readonly_fields = [
        'date_ordered',
        'date_paid',
        'date_shipped',
    ]

    inlines = [OrderItemInline]

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'shipping_full_name',
        'shipping_email',
        'shipping_phone_number',
        'shipping_district'
        'shipping_address1'
        'shipping_state',
    ]
    search_fields = [
        'shipping_full_name',
        'shipping_email',
        'shipping_phone_number',
        'shipping_district',
    ]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'product',
        'user',
        'quantity',
        'price',
        'get_total',
    ]

    search_fields = ['product__name', 'order__full_name']

# Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order AND OrderAdmin
admin.site.register(Order, OrderAdmin)
