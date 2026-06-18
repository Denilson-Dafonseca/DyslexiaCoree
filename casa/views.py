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
from django.conf import settings

from .models import ClothingOrder
from .forms import ClothingOrderForm

import threading
import requests
import time




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
 
def send_vehicle_email(message, subject="New Vehicle Request - Dyslexiacore"):
    try:
        print("EMAIL TRIGGERED (BREVO API)")

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }

        payload = {
            "sender": {
                "name": "Dyslexiacore",
                # Brevo
                "email": "dyslexiacore@gmail.com"
            },
            "to": [
                {"email": "denilkson.dafonseca99@gmail.com"},
                {"email": "gerhaldmutukuta@gmail.com"},
                {"email": "danielesau480@gmail.com"},
                {"email": "thimothshangadi@gmail.com"},
                {"email": "yashesauto@gmail.com"}, 
                {"email": "sheyashingo629@gmail.com"},
                {"email": "tunabutkus@gmail.com"},
                {"email": "lamekmunana6@gmail.com"}, 
                {"email": "mwingarhamesmuhinda@gmail.com"} 
            ],
            "subject": subject,
            "htmlContent": f"""
            <h2>New Vehicle Request</h2>
            <p>{message.replace(chr(10), '<br>')}</p>
            """
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code == 201:
            print("EMAIL SENT SUCCESSFULLY")
            return True

        print("EMAIL FAILED")
        return False

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        return False


def Car_order(request):
    success = False
    form = VehicleRequestForm()

    if request.method == "POST":
        form = VehicleRequestForm(request.POST)

        if form.is_valid():

            # Don't save immediately
            data = form.save(commit=False)

            # Pending by default
            data.status = False

            data.save()

            message = f"""
Name: {data.name}
Phone: {data.phone}
Vehicle: {data.vehicle}
Budget: {data.budget}
Location: {data.location}
Import: {data.iimport}
Description(details): {data.message or 'N/A'}
"""

            send_vehicle_email(message)

            success = True

            messages.success(
                request,
                "Vehicle request submitted successfully."
            )

            return redirect("Car_order")

        else:
            messages.error(
                request,
                "There was an error submitting the request."
            )

    return render(request, "Car_order.html", {
        "form": form,
        "success": success,
    })


def mark_done(request, id):
    data = get_object_or_404(VehicleRequest, id=id)

    # Mark as secured
    data.status = True
    data.save()

    messages.success(
        request,
        f"Request #{data.id} marked as secured."
    )

    return redirect('Car_order')


def Not_secured(request):

    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect("main")

    # Pending requests only
    VehicleRequests = VehicleRequest.objects.filter(
        status=False
    ).order_by('-id')

    if request.method == "POST":

        VehicleRequest_id = request.POST.get(
            "VehicleRequest_id"
        )

        if VehicleRequest_id:

            VehicleRequest.objects.filter(
                id=VehicleRequest_id
            ).update(
                status=True
            )

            messages.success(
                request,
                f"Request #{VehicleRequest_id} marked as secured."
            )

            return redirect("Not_secured")

    return render(
        request,
        "Not_secured.html",
        {
            "VehicleRequests": VehicleRequests
        }
    )


def Secured_deal(request):

    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect("main")

    # Secured requests only
    VehicleRequests = VehicleRequest.objects.filter(
        status=True
    ).order_by('-id')

    if request.method == "POST":

        VehicleRequest_id = request.POST.get(
            "VehicleRequest_id"
        )

        if VehicleRequest_id:

            VehicleRequest.objects.filter(
                id=VehicleRequest_id
            ).update(
                status=False
            )

            messages.success(
                request,
                f"Request #{VehicleRequest_id} moved back to pending."
            )

            return redirect("Secured_deal")

    return render(
        request,
        "Secured_deal.html",
        {
            "VehicleRequests": VehicleRequests
        }
    )
    
    
def send_clothing_email(message, subject="New Clothing Order - Boutique"):
    """Send email notification via Brevo API"""
    try:
        print("EMAIL TRIGGERED (BREVO API)")
        
        url = "https://api.brevo.com/v3/smtp/email"
        
        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }
        
        # Update with your boutique team emails
        payload = {
            "sender": {
                "name": "DyslexiaCore_boutique",
                "email":  "dyslexiacore@gmail.com"
            },
            "to": [
                {"email": "denilkson.dafonseca99@gmail.com"},
                # Add more team emails here
            ],
            "subject": subject,
            "htmlContent": f"""
            <h2>New Clothing Order</h2>
            <div style="background:#f8f9fa; padding:20px; border-radius:10px;">
                {message.replace(chr(10), '<br>')}
            </div>
            <br>
            <p style="color:#6c757d;">This is an automated notification from your Boutique System.</p>
            """
        }
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        
        if response.status_code == 201:
            print("EMAIL SENT SUCCESSFULLY")
            return True
        
        print("EMAIL FAILED")
        return False
        
    except Exception as e:
        print("EMAIL ERROR:", str(e))
        return False

def clothing_order(request):
    form = ClothingOrderForm()
    success = False
    
    if request.method == "POST":
        form = ClothingOrderForm(request.POST)
        
        if form.is_valid():
            # Save the order
            order = form.save(commit=False)
            order.status = 'pending'
            order.save()
            
            # Prepare email message
            message = f"""
🛍️ NEW CLOTHING ORDER
━━━━━━━━━━━━━━━━━━━

 Personal Information:
Name: {order.name}
Email: {order.email}
Phone: {order.phone}

━━━━━━━━━━━━━━━━━━━

Order Details:
Event Type: {order.get_event_type_display()}
Gender: {order.get_gender_display()}
Size: {order.get_size_display()}
{order.custom_size if order.size == 'custom' else ''}

Clothing Type: {order.clothing_type}
Color Preference: {order.color_preference or 'N/A'}
Fabric Preference: {order.fabric_preference or 'N/A'}

━━━━━━━━━━━━━━━━━━━

Event Information:
Event Date: {order.event_date or 'Not specified'}

Budget Range:
Min: N${order.budget_min or 'N/A'}
Max: N${order.budget_max or 'N/A'}

━━━━━━━━━━━━━━━━━━━

 Special Requirements:
{order.special_requirements or 'None specified'}

Additional Notes:
{order.additional_notes or 'None specified'}

━━━━━━━━━━━━━━━━━━━
Order ID: #{order.id}
Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}
Status: {order.get_status_display()}
"""
            
            # Send email notification
            subject = f"New Clothing Order #{order.id} - {order.name}"
            send_clothing_email(message, subject)
            
            messages.success(
                request,
                "🎉 Your clothing order has been submitted successfully! We'll contact you within 24 hours."
            )
            
            return redirect('clothing_order')
        else:
            messages.error(
                request,
                " There was an error submitting your order. Please check the form."
            )
    
    return render(request, "clothing_order.html", {
        "form": form,
        "success": success,
    })

