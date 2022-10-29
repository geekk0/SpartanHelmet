from django.db import models
from cart.funcs import get_exchange_rate


class Currencies(models.Model):
    name = models.CharField(default="валюта ...", max_length=24, verbose_name="Название валюты")
    exchange_rate = models.DecimalField(verbose_name="курс обмена к рублю", decimal_places=2, max_digits=10, blank=True,
                                        null=True)
    url = models.TextField(verbose_name="страница курса валюты", blank=True, null=True)

    def get_currency_url(self):
        self.url = "https://www.google.com/search?q=курс+" + self.name + "+к+рублю"

    def __str__(self):
        return self.name + " " + str(self.id)

    def update_current_rate(self, url):
        self.get_currency_url()
        current_exchange = get_exchange_rate(url)
        self.exchange_rate = current_exchange

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
