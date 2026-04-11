from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, CarouselSlide, Category, Profile, Relief, Video


from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from cart.cart import Cart
from pay.forms import ShippingForm
from pay.models import ShippingAddress, Order, OrderItem
from django import forms
import json
from django.db.models import Q

from django.core.mail import send_mail
from .forms import VehicleRequestForm
from .models import VehicleRequest

from django.utils import timezone
import threading
from django.conf import settings

import threading




def main(request):
    slides = CarouselSlide.objects.all()  # Always load slides
    
    context = {'slides': slides}  # Base context

    if request.method == "POST":
        searched = request.POST.get('searched', '')
        
        if searched:  
            products = Product.objects.filter(name__icontains=searched)
            if products.exists():
                context['searched'] = products
            else:
                messages.error(request, "That product does not exist")
        else:
            messages.warning(request, "Please enter a search term")

    return render(request, "main.html", context)

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('main')


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, " Update successful")
			return redirect('main')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('main')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password,)
        if user is not None:
            login(request, user)
            
        # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value) 
            
            messages.success(request, ("You have logged into your account"))
            return redirect('main')
        else:
             messages.success(request, ("An Error has occurred try again"))
             return redirect('login')
            
    else:
        return render(request, "login.html", {})    
       
def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out"))
    return redirect('/')

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	
 
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password, email=email)
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("here was a problem Registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

def category(request,bk):
    bk = bk.replace('-', ' ')
    try:
        category = Category.objects.get(name=bk)
        products = Product.objects.filter(category=category,is_available=True)
        return render(request, 'category.html', {'products':products, 'category':category})
    except: 
        messages.success(request, ("No product on that page"))
        return redirect('/')  
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def stand(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'stand.html', {'products':products})

def info(request):
    videos = Video.objects.all()
    return render(request, 'info.html', {'videos': videos})
 

def door_to_door_relief(request):
    doors = Relief.objects.all()
    context = {"doors": doors}    
    return render(request, 'door_to_door_relief.html', context)


def payment_method(request):
    
    return render(request, 'payment_method.html',{})

def advert(request):
    
    return render(request, 'advert.html',{})

def Affiliate(request):
    
    return render(request, 'Affiliate.html',{})

def Credit(request):
    
    return render(request, 'Credit.html',{})

def Vendor(request):
    
    return render(request, 'Vendor.html',{})

def Purchasing_steps(request):
    
    return render(request, 'Purchasing_steps.html',{})

def Privacy_Policy(request):
    
    return render(request, 'Privacy_Policy.html',{})

def Terms_of_service(request):
    
    return render(request, 'Terms_of_service.html',{}) 
 
    

def send_vehicle_email(message):
    try:
        print("EMAIL TRIGGERED")

        send_mail(
            subject="🚗 New Vehicle Request - Dyslexiacore",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                "denilkson.dafonseca99@gmail.com",
                "danielesau480@gmail.com",
                "yashesauto@gmail.com",
                "tunabutkus@gmail.com",
                "thimothshangadi@gmail.com",
                "gerhaldmutukuta@gmail.com",
                "alfarythms@gmail.com",
                "hambekombada@gmail.com"
            ],
            fail_silently=False,
        )

        print("EMAIL SENT")

    except Exception as e:
        print("EMAIL ERROR:", str(e))


# 🚀 MAIN VIEW
def Car_order(request):
    success = False
    form = VehicleRequestForm()

    if request.method == "POST":
        form = VehicleRequestForm(request.POST)

        if form.is_valid():
            data = form.save()

            message = f"""
🔥 NEW VEHICLE LEAD

Name: {data.name}
Phone: {data.phone}
Vehicle: {data.vehicle}
Budget: {data.budget}

Message:
{data.message or 'N/A'}
"""

            # 🚀 NON-BLOCKING EMAIL (SAFE THREAD)
            threading.Thread(
                target=send_vehicle_email,
                args=(message,),
                daemon=True
            ).start()

            success = True

    return render(request, "Car_order.html", {
        "form": form,
        "success": success
    })


# DONE BUTTON VIEW
def mark_done(request, id):
    data = get_object_or_404(VehicleRequest, id=id)
    data.status = "completed"
    data.save()
    
    return redirect('Car_order')
