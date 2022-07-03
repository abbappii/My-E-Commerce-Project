
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

# # models and forms
from App_Order.models import Order, Cart
from App_Payment.forms import BillingAddress, BillingForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

# import requests
# from sslcommerz_python.payment import SSLCSession
# from decimal import Decimal
# import socket

# from django.views.decorators.csrf import csrf_exempt
# # Create your views here.


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(data=request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, "Shipping address saved!!")

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # orderitems er sob gulo object ke call kora
    order_items = order_qs[0].orderitems.all()
    # get_totals ke call kora , order_qs er object
    order_total = order_qs[0].get_totals()

    return render(request, 'App_Payment/checkout.html', context={'form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address': saved_address})

import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
# from django.conf import settings
from My_Ecommerce_Project import settings


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, 'Please complete shipping address.')
        return redirect('App_Payment:checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request,'Please complete your profile details')
        return redirect('App_Login:profile')

    mypayment = SSLCSession(sslc_is_sandbox=True,
        sslc_store_id=settings.store_id,
        sslc_store_pass=settings.Api_key
    )

    status_url = request.build_absolute_uri(reverse('App_Payment:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_item_count = order_items.order_items.count()
    total = order_qs[0].get_totals()
    
    mypayment.set_product_integration(total_amount=Decimal(total), 
        currency='BDT', product_category='Mixed', 
        product_name=order_items, num_of_item=order_item_count, 
        shipping_method='C', product_profile='None'
    )

    user = request.user
    mypayment.set_customer_info(name=user.profile.full_name, 
        email=user.email, 
        address1=user.profile.address_1, 
        address2=user.profile.address_1,
        city=user.profile.city, 
        postcode=user.profile.zipcode, 
        country=user.profile.country, 
        phone=user.profile.phone
    )

    mypayment.set_shipping_info(
        shipping_to= user.profile.full_name , 
        address= saved_address.address, 
        city= saved_address.city, 
        postcode=saved_address.zipcode, 
        country=saved_address.country
        )
    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])

    
    
        
# @login_required
# def payment(request):
#     saved_address = BillingAddress.objects.get_or_create(user=request.user)
#     saved_address = saved_address[0]
#     if not saved_address.is_fully_filled():
#         messages.info(request, f"Please complete shipping address!")
#         return redirect("App_Payment:checkout")

#     if not request.user.profile.is_fully_filled():
#         messages.info(request, f"Please complete profile details!")
#         return redirect("App_Login:profile")

    # store_id = 'abc603cbc56e0f77'
    # Api_key = 'abc603cbc56e0f77@ssl'

#     mypayment = SSLCSession(sslc_is_sandbox=True,
#                             sslc_store_id=store_id, sslc_store_pass=Api_key)

#     status_url = request.build_absolute_uri(reverse("App_Payment:complete"))
#     # print(status_url)

    # mypayment.set_urls(success_url=status_url, fail_url=status_url,
    #                    cancel_url=status_url, ipn_url=status_url)

#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     order_items = order_qs[0].orderitems.all()
#     order_items_count = order_qs[0].orderitems.count()
#     order_total = order_qs[0].get_totals()

#     mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
#                                       product_name=order_items, num_of_item=order_items_count, shipping_method='courier', product_profile='None')

#     currnet_user = request.user
    # mypayment.set_customer_info(name=currnet_user.profile.full_name, email=currnet_user.email, address1=currnet_user.profile.address_1, address2=currnet_user.profile.address_1,
    #                             city=currnet_user.profile.city, postcode=currnet_user.profile.zipcode, country=currnet_user.profile.country, phone=currnet_user.profile.phone)

#     mypayment.set_shipping_info(shipping_to=currnet_user.profile.full_name, address=saved_address.address,
#                                 city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

#     response_data = mypayment.init_payment()

#     return redirect(response_data['GatewayPageURL'])


# @csrf_exempt
# def complete(request):
#     if request.method == 'POST' or request.method == 'post':
#         payment_data = request.POST
#         status = payment_data['status']

#         if status == 'VALID':
#             val_id = payment_data['val_id']
#             tran_id = payment_data['tran_id']
#             messages.success(
#                 request, f"Your payment Completed successfully! Page will be redirect after 5 seconds.")
#             return HttpResponseRedirect(reverse("App_Payment:purchase", kwargs={'val_id': val_id, 'tran_id': tran_id}))

#         elif status == 'FAILED':
#             messages.warning(
#                 request, f"Your payment failed! please try again!! Page will be redirect after 5 seconds.")

#     return render(request, 'App_Payment/complete.html', context={})


# @login_required
# def purchase(request, val_id, tran_id):
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     order = order_qs[0]
#     orderId = tran_id
#     order.ordered = True
#     order.orderId = orderId
#     order.paymentId = val_id
#     order.save()
#     cart_items = Cart.objects.filter(user=request.user, purchased=False)
#     for item in cart_items:
#         item.purchased = True
#         item.save()

#     return HttpResponseRedirect(reverse('App_Shop:home'))


# @login_required
# def order_view(request):
#     try:
#         orders = Order.objects.filter(user=request.user,ordered = True)
#         context = {'orders':orders}

#     except:
#         messages.warning(request,"You do not have an active order")
#         return redirect('App_Shop:home')
#     return render(request,"App_Payment/order.html",context)


