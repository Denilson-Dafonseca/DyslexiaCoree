from django.db import models
import datetime
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

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)
    
# Category     
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Meta:
    verbose_name_plural = 'Categories'    
    
# Cutomers    
class Customer(models.Model):
    first_name = models.CharField(max_length=100, default="client")
    last_name = models.CharField(max_length=100, default="client")
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
   
    def __str__(self):
        return f'{self.first_name} {self.sur_name}'   
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    image = models.ImageField(upload_to='media/')
    #sales
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_available = models.BooleanField(default=True)



    def __str__(self):
        return self.name  
        
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250, default="", blank=True)
    phone = models.CharField(max_length=100, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)  

    def __str__(self):
        return self.product        
        
class CarouselSlide(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/')
    is_active = models.BooleanField(default=True)  # Optional: for toggling visibility

    def __str__(self):
        return self.title
    
class Relief(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    image = models.ImageField(upload_to='media/')
  
    def __str__(self):
        return self.name
    
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="Paste a YouTube link here.")
    video_file = models.FileField(upload_to='media/', blank=True, null=True, help_text="Or upload a video file.")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_embed_url(self):
        """
        Converts a normal YouTube link into an embeddable link
        (e.g. https://www.youtube.com/watch?v=abc123 → https://www.youtube.com/embed/abc123)
        """
        if self.youtube_url:
            return self.youtube_url.replace("watch?v=", "embed/")
        return None
    
  