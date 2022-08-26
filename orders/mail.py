import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Order, OrderItem
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .bot import send_telegram_order_notification


def send_customer_confirmation_email(order):

    msg = MIMEMultipart()
    msg['Subject'] = 'Order ' + order.first_name + " in Spartan-helmet store."
    msg['From'] = "Spartan-helmet <gekk0test@yandex.ru>"
    msg['To'] = order.email
    send_to = [order.email]
    text = MIMEText("Your order №" + str(order.id) + " is being processed. You will be contacted shortly ")
    msg.attach(text)

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    # server.ehlo()
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(msg['From'], send_to, msg.as_string())
    server.quit()

    return HttpResponseRedirect('/')


def send_notify_order_email(order, request):

    msg = MIMEMultipart()
    msg['Subject'] = 'Новый заказ от ' + order.first_name + " №" + str(order.id)
    msg['From'] = "Spartan-helmet <gekk0test@yandex.ru>"
    msg['To'] = "gekk0test@yandex.ru"
    send_to = ["gekk0test@yandex.ru"]

    customer_info_dict = {
        "Имя": order.first_name,
        "Фамилия": order.last_name,
        "E-mail": order.email,
        "Страна": order.country,
        "Город": order.city,
        "Адрес": order.address,
        "Почтовый индекс": order.postal_code,
        "Телефон": str(order.phone_number)
    }

    customer_info_block = format_customer_info(customer_info_dict)

    order_items_block = format_order_items(order)

    if not request.user.username:
        request.user.username = "неизвестный"

    send_telegram_order_notification("Новый заказ №" + str(order.id) + " от " + request.user.username + "!\n" +
                                     customer_info_block + "\n" + order_items_block)

    text = MIMEText(customer_info_block + "\n" + order_items_block)
    msg.attach(text)

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(msg['From'], send_to, msg.as_string())
    server.quit()

    return HttpResponseRedirect('/')


def format_customer_info(customer_info_dict):
    customer_info_block = ""
    for k, v in customer_info_dict.items():
        customer_info_block += k + ": " + v + "\n"

    return customer_info_block


def format_order_items(order):
    order_items_block = ""
    for order_item in OrderItem.objects.filter(order=order):
        order_items_block += "Товар: " + order_item.product.name + " x" + str(order_item.quantity) + "\n"
    return order_items_block

