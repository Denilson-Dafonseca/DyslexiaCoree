from django.shortcuts import render, redirect
from cart.cart import Cart
from pay.forms import ShippingForm, PaymentForm
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
        # Save shipping info in session
        request.session['my_shipping'] = request.POST

        # Placeholder for future payment method integration (e.g., Stripe)
        messages.info(request, "Payment processing method not configured yet.")
        return redirect("checkout")

    else:
        messages.error(request, "Access Denied")
        return redirect("main")


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('main')

        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('main')
    
def ewallet_checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        payment_option = request.POST.get('payment_option')
        total = cart.get_total()

        # Create ShippingAddress entry
        shipping = ShippingAddress.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            zipcode=zip_code,
        )

        # Create Order (not shipped yet)
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            shipping_address=shipping,
            amount_paid=total,
            shipped=False,
            date_ordered=datetime.datetime.now(),
            payment_method=payment_option
        )

        # Optionally save cart items into OrderItems if your model supports it
        cart.clear()

        messages.success(request, "Order submitted successfully! Please send payment to the selected e-wallet.")
        return redirect('main')  # or redirect to a thank-you page

    return render(request, 'payment/ewallet_checkout.html', {'cart': cart})


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('main')

        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('main')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}"
        )
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            Profile.objects.filter(user__id=request.user.id).update(old_cart="")

            messages.success(request, "Order Placed!")
            return redirect('main')

        else:
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Order Placed!")
            return redirect('main')


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
