from django.shortcuts import render, redirect
from cart.cart import Cart
from pay.forms import ShippingForm, PaymentForm
from pay.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from casa.models import Product, Profile
# PAYPAL INFO
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

import uuid
import datetime


    

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('main')


		return render(request, 'payment/orders.html', {"order":order, "items":items})

	else:
		messages.success(request, "Access Denied")
		return redirect('main')


def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = float(cart.cart_total())  # Make sure it's a float, not a Decimal or string

    if request.method == "POST":
        # Save shipping info in session
        request.session['my_shipping'] = request.POST

        host = request.get_host()
        invoice = str(uuid.uuid4())

        # ✅ Format amount properly — PayPal expects a string with 2 decimal places
        formatted_total = "{:.2f}".format(totals)

        # ✅ Make sure your settings.py has:
        # PAYPAL_RECEIVER_EMAIL = "your-paypal-business-email@example.com"

        # ✅ Use NAD only if your business account supports it.
        # If not, use USD — many errors come from unsupported currency.
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": formatted_total,
            "item_name": "DyslexiaCore Order",
            "invoice": invoice,
            "currency_code": "NAD",  # or "USD" if NAD not supported by your PayPal account
            "notify_url": f"https://{host}{reverse('paypal-ipn')}",
            "return_url": f"https://{host}{reverse('payment_success')}",
            "cancel_return": f"https://{host}{reverse('payment_failed')}",
            "custom": str(request.user.id) if request.user.is_authenticated else "Guest",
            "no_shipping": "1",  # 0 = address required, 1 = no address, 2 = prompt but optional
        }

        # ✅ Create PayPal form
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        billing_form = PaymentForm()

        return render(
            request,
            "payment/billing_info.html",
            {
                "paypal_form": paypal_form,
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": formatted_total,
                "shipping_info": request.POST,
                "billing_form": billing_form,
            },
        )

    else:
        messages.error(request, "Access Denied")
        return redirect("main")



def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('main')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('main')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('main')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('main')

def process_order(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")


			messages.success(request, "Order Placed!")
			return redirect('main')

			

		else:
			# not logged in
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('main')


def payment_success(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    # Delete purchased products
    for product in cart_products:
        try:
            product_name = product.name
            product.delete()
            print(f"Deleted product after purchase: {product_name}")
        except Exception as e:
            print(f" Error deleting {product.name}: {e}")

    # Clear the session cart
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    # Clear old cart data for logged-in users
    if request.user.is_authenticated:
        Profile.objects.filter(user__id=request.user.id).update(old_cart="")

    messages.success(request, "Payment successful! Purchased items have been removed from the store.")
    return render(request, "payment/payment_success.html", {})


def payment_failed(request):
    
    return render(request, "payment/payment_failed.html", {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm(request.POST or None)
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(
        request,
        "payment/checkout.html",
        {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form,
        }
    )


