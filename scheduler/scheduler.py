import socket
import sys

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from cart.funcs import get_exchange_rate
from django.conf import settings
from currencies.models import Currencies


def update_currencies_exchange_rate():
    for currency in Currencies.objects.all():
        currency.update_current_rate(currency.url)
        currency.save()


def start():

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        print("!!!scheduler already started, DO NOTHING")
    else:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.start()

        scheduler.add_job(update_currencies_exchange_rate, 'interval', minutes=1,
                          start_date=datetime.strptime('Oct 15 2021  9:10AM', '%b %d %Y %I:%M%p'),
                          id='update_usdt_exchange_rate',
                          jobstore='default', replace_existing=True, max_instances=1, coalesce=True)

        print("Scheduler started...", file=sys.stdout)
