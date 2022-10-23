from django.shortcuts import render
from .models import OrderItem, UserInfo, Order
from .forms import OrderCreateForm, UserInfoUpdateForm
from cart.cart import Cart
from .mail import send_customer_confirmation_email, send_notify_order_email, send_customer_order_status
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.phone_number = form.cleaned_data['phone']
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         weight=item['weight'])
            # очистка корзины

            cart.clear()

            save_info = request.POST.get('save_info')

            if save_info == "True" and request.user.is_authenticated:
                add_order_info_to_user_info(request, order)

            send_customer_confirmation_email(order)
            send_notify_order_email(order, request)

            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:

        if not request.user.is_authenticated:
            form = OrderCreateForm
        else:

            if UserInfo.objects.filter(user=request.user).count() > 0:
                customer_info = UserInfo.objects.get(user=request.user)
                form = OrderCreateForm(initial={
                    'first_name': customer_info.first_name, 'last_name': customer_info.last_name,
                    'email': customer_info.email, 'phone': customer_info.phone_number, 'country': customer_info.country,
                    'city': customer_info.city, 'address': customer_info.address, 'postal_code': customer_info.postal_code
                })

            else:
                form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


def add_order_info_to_user_info(request, order):
    customer = request.user

    if not len(UserInfo.objects.filter(user=customer)) > 0:
        customer_info = UserInfo.objects.create(user=customer)
    else:
        customer_info = UserInfo.objects.get(user=request.user)

    customer_info.first_name = order.first_name
    customer_info.last_name = order.last_name
    customer_info.email = order.email
    customer_info.phone_number = order.phone_number
    customer_info.postal_code = order.postal_code
    customer_info.address = order.address
    customer_info.city = order.city
    customer_info.country = order.country
    customer_info.save()


def account_details(request):
    customer = request.user

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/Showcase")
    if UserInfo.objects.filter(user=customer).count() > 0:
        customer_info = UserInfo.objects.get(user=customer)
    else:
        return HttpResponseRedirect("edit_account_details")

    return render(request, "orders/account_details.html", {"customer": customer, "customer_info": customer_info})


def edit_account_details(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/Showcase")

    if request.method == 'POST':
        form = UserInfoUpdateForm(request.POST)
        if form.is_valid():
            customer_form_info = form.save()
            customer_form_info.phone_number = form.cleaned_data['phone']
            customer_form_info.user = request.user

            if UserInfo.objects.filter(user=request.user).count() > 0:

                customer_info = UserInfo.objects.get(user=request.user)

                customer_info.first_name = customer_form_info.first_name
                customer_info.last_name = customer_form_info.last_name
                customer_info.email = customer_form_info.email
                customer_info.country = customer_form_info.country
                customer_info.city = customer_form_info.city
                customer_info.address = customer_form_info.address
                customer_info.phone_number = customer_form_info.phone_number
                customer_info.postal_code = customer_form_info.postal_code

                customer_info.save()
                customer_form_info.delete()

            else:

                customer_form_info.save()

            return HttpResponseRedirect("account_details")
    else:
        if UserInfo.objects.filter(user=request.user).count() > 0:
            customer_info = UserInfo.objects.get(user=request.user)
            form = UserInfoUpdateForm(initial={
                'first_name': customer_info.first_name, 'last_name': customer_info.last_name,
                'email': customer_info.email, 'phone': customer_info.phone_number, 'country': customer_info.country,
                'city': customer_info.city, 'address': customer_info.address, 'postal_code': customer_info.postal_code
            })
        else:
            form = UserInfoUpdateForm

        return render(request, "orders/edit_account_details.html", {"form": form})


def customer_orders(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/Showcase")

    customer = request.user
    customer_orders = Order.objects.filter(user=customer)
    last_order = customer_orders.order_by("-created").first()
    last_order_items = OrderItem.objects.filter(order=last_order)

    all_orders = Order.objects.all()

    return render(request, "orders/customer_orders.html", {"customer": customer, "customer_orders": customer_orders,
                            "last_order": last_order, "last_order_items": last_order_items, "all_orders": all_orders})


def update_order_status(request, order_id):

    status = request.GET.get("status_input")

    order_object = Order.objects.get(id=order_id)

    order_object.status = status

    order_object.save()

    send_customer_order_status(order_object)

    return HttpResponse(status=204)


