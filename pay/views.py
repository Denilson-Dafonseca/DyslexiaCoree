from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User

from cart.cart import Cart

from pay.models import ShippingAddress, Order, OrderItem
from pay.forms import ShippingForm
from casa.models import Product, Profile
from django.conf import settings

import threading


def orders(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect("main")

    order = get_object_or_404(Order, id=pk)
    items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        status = request.POST.get("shipping_status")
        now = timezone.now()
        if status == "true":
            order.shipped = True
            order.date_shipped = now
        else:
            order.shipped = False
            order.date_shipped = None
        order.save()
        messages.success(request, "Shipping status updated.")
        return redirect("orders", pk=order.id)

    return render(request, "payment/orders.html", {"order": order, "items": items})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.method == "POST":
        # Get shipping and payment info
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        district = request.POST.get("district")
        payment_method = request.POST.get("payment_method")  # e-wallet, etc.

        # Create shipping address
        shipping = ShippingAddress.objects.create(
            user=request.user if request.user.is_authenticated else None,
            shipping_full_name=full_name,
            shipping_email=email,
            shipping_phone_number=phone_number,
            shipping_address1=address,
            shipping_district=district,
        )

        # Create the order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=address,
            amount_paid=totals,
            payment_method=payment_method,
            paid=False,
            date_ordered=timezone.now(),
        )

        # Create order items and mark products as unavailable
        for product in cart_products:
            product_obj = Product.objects.get(id=product.id)
            quantity = quantities.get(str(product.id), 1)
            price = product_obj.sale_price if product_obj.is_sale else product_obj.price

            OrderItem.objects.create(
                order=order,
                product=product_obj,
                user=request.user if request.user.is_authenticated else None,
                quantity=quantity,
                price=price,
            )

            # Soft delete: mark product as unavailable
            product_obj.is_available = False
            product_obj.save()

            # Remove product from cart session
            cart.delete(product_obj.id)

        # Clear saved cart data from user profile if logged in
        if request.user.is_authenticated:
            Profile.objects.filter(user=request.user).update(old_cart="")

        # Save shipping info in session for receipt page
        request.session["shipping_info"] = {
            "shipping_full_name": full_name,
            "shipping_email": email,
            "shipping_phone": phone_number,
            "shipping_address1": address,
            "shipping_district": district,
        }

        return redirect("order_placed")

    # GET request → show checkout page
    return render(
        request,
        "payment/checkout.html",
        {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
        },
    )
    

def not_paid_dash(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect("main")

    orders = Order.objects.filter(paid=False)

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            Order.objects.filter(id=order_id).update(paid=True, date_paid=timezone.now())
            messages.success(request, f"Order #{order_id} marked as paid.")
            return redirect("not_paid_dash")

    return render(request, "payment/not_paid_dash.html", {"orders": orders})


def paid_dash(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect("main")

    orders = Order.objects.filter(paid=True)

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            Order.objects.filter(id=order_id).update(paid=False, date_paid=None)
            messages.success(request, f"Order #{order_id} reverted to unpaid.")
            return redirect("paid_dash")

    return render(request, "payment/paid_dash.html", {"orders": orders})


def order_placed(request):
    messages.success(request, "Order placed successfully.")
    return render(request, "payment/order_placed.html")

def receipt(request):
    # Get the latest order for the current user (or last session)
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user).order_by('-date_ordered').first()
    else:
        # For guests, you might store the order id in the session
        order = Order.objects.filter(user=None).order_by('-date_ordered').first()        

    if not order:
        return render(request, "payment/receipt.html", {
            "cart_products": [],
            "quantities": {},
            "totals": 0,
        })

    # Get order items
    order_items = OrderItem.objects.filter(order=order)

    # Prepare quantities dict
    quantities = {item.product.id: item.quantity for item in order_items}

    # Prepare totals
    totals = sum(item.price * item.quantity for item in order_items)

  

    return render(request, "payment/receipt.html", {
        "cart_products": [item.product for item in order_items],
        "quantities": quantities,
        "totals": totals,
    })
    
