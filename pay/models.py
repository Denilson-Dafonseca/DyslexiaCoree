from django.db import models
from django.contrib.auth.models import User
from casa.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


# -------------------------------
# SHIPPING ADDRESS MODEL
# -------------------------------
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_phone_number = models.CharField(max_length=10, blank=True)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_district = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    date_shipped = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"{self.shipping_full_name} - {self.shipping_district}"

# Auto-create a shipping address profile when a new user registers
@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)

# -------------------------------
# ORDER MODEL
# -------------------------------
class Order(models.Model):
    PAYMENT_METHODS = [
        ("FNB eWallet", "FNB eWallet"),
        ("Bank Windhoek EasyWallet", "Bank Windhoek EasyWallet"),
        ("Standard Bank PayPulse", "Standard Bank PayPulse"),
        ("Visa / Mastercard", "Visa / Mastercard"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHODS, null=True, blank=True
    )
    payment_reference = models.CharField(
        max_length=100, null=True, blank=True, help_text="E-Wallet or Bank reference number"
    )
    paid = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    class Meta:
        ordering = ["-date_ordered"]

# -------------------------------
# ORDER ITEM MODEL
# -------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order Items - {str(self.id)}'
