from django.shortcuts import render, redirect
from cart.cart import Cart
from pay.forms import ShippingForm
from pay.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from casa.models import Product, Profile
import datetime

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                now = datetime.datetime.now()
                order = Order.objects.filter(id=pk)
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('main')

        return render(request, 'payment/orders.html', {"order": order, "items": items})

    else:
        messages.success(request, "Access Denied")
        return redirect('main')

def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = float(cart.cart_total())

    if request.method == "POST":
        # Save shipping info in session for later processing
        request.session['my_shipping'] = request.POST.dict()  # safer conversion
        messages.success(request, "Shipping info saved. Proceed to payment.")
        return redirect('checkout')  # redirect to your checkout/payment page

    # Allow GET requests to display billing form
    return render(
        request,
        'payment/billing_info.html',
        {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
        }
    )

def payment_success(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    for product in cart_products:
        try:
            product_name = product.name
            product.delete()
            print(f"Deleted product after purchase: {product_name}")
        except Exception as e:
            print(f"Error deleting {product.name}: {e}")

    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

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

    # Pull shipping info from session if available
    shipping_info = request.session.get('my_shipping', {})

    if request.method == "POST":
        full_name = request.POST.get('full_name') or shipping_info.get('full_name')
        email = request.POST.get('email') or shipping_info.get('email')
        phone_number = request.POST.get('phone_number') or shipping_info.get('phone_number')
        address = request.POST.get('address') or shipping_info.get('address_1')
        city = request.POST.get('city') or shipping_info.get('city')
        zip_code = request.POST.get('zip_code') or shipping_info.get('zipcode')
        payment_option = request.POST.get('payment_option')
        total = cart.cart_total()

        # Create ShippingAddress record
        shipping = ShippingAddress.objects.create(
            user=request.user if request.user.is_authenticated else None,
            shipping_full_name=full_name,
            shipping_email=email,
            shipping_phone_number=phone_number,
            shipping_address1=address,
            shipping_city=city,
            shipping_zipcode=zip_code,
            shipping_country=shipping_info.get('country', 'Namibia')
        )

        # Create Order record (not paid yet)
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=f"{address}, {city}, {zip_code}",
            amount_paid=total,
            paid=False,
            payment_method=payment_option,
            date_ordered=datetime.datetime.now()
        )

        # Clear cart after submission
        cart.clear()
        messages.success(request, "Order submitted! Please send payment to the selected e-wallet.")
        return redirect('not_paid_dash')

    return render(request, 'payment/ewallet_checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_info': shipping_info
    })



def not_paid_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(paid=False)
        if request.method == "POST":
            order_id = request.POST.get('order_id')
            Order.objects.filter(id=order_id).update(paid=True, date_paid=datetime.datetime.now())
            messages.success(request, "Payment status updated to PAID.")
            return redirect('not_paid_dash')
        return render(request, "payment/not_paid_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access denied.")
        return redirect('main')


def paid_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(paid=True)
        if request.method == "POST":
            order_id = request.POST.get('order_id')
            Order.objects.filter(id=order_id).update(paid=False, date_paid=None)
            messages.success(request, "Payment status reverted to UNPAID.")
            return redirect('paid_dash')
        return render(request, "payment/paid_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access denied.")
        return redirect('main')

    