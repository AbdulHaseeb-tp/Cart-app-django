from django.shortcuts import render, redirect
from . models import Order,OrderdItem
from django.contrib import messages
from products.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

def show_cart(request):
    user=request.user  # which user is ..
    customer=user.customer_profile # reverse relationship of Customer
    
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
    context={'cart':cart_obj}
    return render(request, 'cart.html', context)


@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user  # which user is ..
        customer=user.customer_profile # reverse relationship of Customer 
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')

        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Product.objects.get(pk=product_id) 
        ordered_item,created=OrderdItem.objects.get_or_create(
            product=product,
            owner=cart_obj
        )
        # same quantities adding in cart 
        if created: # not a same
            ordered_item.quantity=quantity
            ordered_item.save()
        else: # same quantity
            ordered_item.quantity=ordered_item.quantity + quantity
            ordered_item.save()
    return redirect('cart')


# Remove a  quantity from the cart

def remove_item_from_cart(request,pk):
    item=OrderdItem.objects.get(pk=pk)
    if item: # if item existing
        item.delete()
    return redirect('cart')

# check out page checking

def checkout_cart(request):
    if request.POST:
        try:
            user=request.user  # which user is ..
            customer=user.customer_profile # reverse relationship of Customer 
            total=float(request.POST.get('total'))

            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                status_message="Your order is Processed, Your item will be delivered with in 2 days"
                messages.success(request,status_message)
            else:
                error_message="Unable to processed, No items in your cart"
                messages.error(request,error_message)    
        except Exception as e:
                error_message="Unable to processed"
                messages.error(request,error_message)

    return redirect('cart')


# orders view page

@login_required(login_url='account')
def view_orders(request):
    user=request.user  # which user is ..
    customer=user.customer_profile # reverse relationship of Customer
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    
    context={'all_orders':all_orders}
    return render(request, 'orders.html', context)