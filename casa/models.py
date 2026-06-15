from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create a user profile when user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)

# Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.URLField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=100, default="client")
    last_name = models.CharField(max_length=100, default="client")
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Carousel Images
class CarouselSlide(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField(blank=True)
    image = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Relief items
class Relief(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.URLField()

    def __str__(self):
        return self.name

# Videos
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_embed_url(self):
        if self.youtube_url:
            return self.youtube_url.replace("watch?v=", "embed/")
        return None
    
# models.py
from django.db import models

class VehicleRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    vehicle = models.CharField(max_length=100)
    budget = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default="Windhoek")
    iimport = models.CharField(max_length=50, default="no")

    message = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.vehicle}"
    
