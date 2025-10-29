from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib.auth.models import User
from pay.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from casa.models import Product, Profile
from django.utils import timezone
from casa.models import Product

def orders(request, pk):
    if not request.user.is_superuser:
        order = Order.objects.get(id=pk) 
        items = OrderItem.objects.filter(order=pk)
     
        
        if request.POST:
            status = request.POST.get('shipping_status') 
            now = timezone.now() 
            if status == "true":
                Order.objects.filter(id=pk).update(shipped=True, date_shipped=now) 
        
            else:
                Order.objects.filter(id=pk).update(shipped=False, date_shipped=None) 
                messages.success(request, "Shipping Status Updated") 
            return redirect('main') 
            

        return render(request, 'payment/orders.html', {"order": order, "items": items})
        
    messages.error(request, "Access Denied") 
    return redirect('main')


def checkout(request):

    
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment_option = request.POST.get('payment_option')

        if not payment_option:
            messages.error(request, "Please select a payment method.")
            return redirect("checkout")

        # Create shipping
        if request.user.is_authenticated:
            shipping = ShippingAddress.objects.create(
            user=request.user,
            shipping_full_name=full_name,
            shipping_email=email,
            shipping_phone_number=phone_number,
            shipping_address1=address,
            shipping_city=city,
            shipping_country="Namibia"
        )
        else:
            shipping = ShippingAddress.objects.create(
            shipping_full_name=full_name,
            shipping_email=email,
            shipping_phone_number=phone_number,
            shipping_address1=address,
            shipping_city=city,
            shipping_country="Namibia"
        )    
      
        # Create order
        if request.user.is_authenticated:
            order = Order.objects.create(
            full_name=full_name,
            email=email,
            shipping_address=address,
            amount_paid=totals,
            payment_method=payment_option,
            paid=False,
            date_ordered=timezone.now()
        )
        else:
            order = Order.objects.create(
            full_name=full_name,
            email=email,
            shipping_address=address,
            amount_paid=totals,
            payment_method=payment_option,
            paid=False,
            date_ordered=timezone.now()
        )
            

        # Add items
        for product in cart_products:
            product_obj = Product.objects.get(id=product.id)
            quantity = quantities.get(str(product.id))
            price = product_obj.sale_price if product_obj.is_sale else product_obj.price
            
        if request.user.is_authenticated:
            OrderItem.objects.create(
                order=order,
                product=product_obj,
                user=request.user,
                quantity=quantity,
                price=price
            )
        else:
            messages.success(request, "You must be logged in to make an order!!!")
            return redirect("register")
            
            
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(
            user=request.user,
            full_name=full_name,
            email=email,
            shipping_address=address,
            amount_paid=totals,
            payment_method=payment_option,
            paid=False,
            date_ordered=timezone.now())
            create_order.save()
            
        else:
             # logged in
            create_order = Order(
            full_name=full_name,
            email=email,
            shipping_address=address,
            amount_paid=totals,
            payment_method=payment_option,
            paid=False,
            date_ordered=timezone.now())
            create_order.save()
              

		# Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=address, amount_paid=totals)
            create_order.save()

            # Add order items
            
            # Get the order ID
            order_id = create_order.pk
            

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")
            
            return redirect('order_placed')

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=address, amount_paid=totals)
            create_order.save()

            # Add order items
            
            # Get the order ID
            order_id = create_order.pk

            # Get quantity
            for key,value in quantities().items():
                if int(key) == product.id:
                    # Create order item
                    create_order_item = OrderItem(order_id=order_id, quantity=value, price=price)
                    create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            messages.success(request, "Order Placed!")
            return redirect('order_placed')



    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
    })


def not_paid_dash(request):
    if not (request.user.is_superuser):
        messages.error(request, "Access denied.")
        return redirect('main')

    order = Order.objects.filter(paid=False)

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        if order_id:
            Order.objects.filter(id=order_id).update(paid=True, date_paid=timezone.now())
            messages.success(request, f"Order #{order_id} marked as paid.")
            return redirect('not_paid_dash')

    return render(request, "payment/not_paid_dash.html", {"order": order})


def paid_dash(request):
    if not (request.user.is_superuser):
        messages.error(request, "Access denied.")
        return redirect('main')

    order = Order.objects.filter(paid=True)

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        if order_id:
            Order.objects.filter(id=order_id).update(paid=False, date_paid=None)
            messages.success(request, f"Order #{order_id} reverted to unpaid.")
            return redirect('paid_dash')

    return render(request, "payment/paid_dash.html", {"order": order})


def order_placed(request):
    if request.user.is_authenticated and request.user.is_superuser:
         
        messages.success(request, "Order placed successfully")
    return render(request, 'payment/order_placed.html')
