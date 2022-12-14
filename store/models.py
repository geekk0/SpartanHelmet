from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from currencies.models import Currencies
from decimal import Decimal

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название категории")
    image = models.ImageField(verbose_name="Обложка", upload_to="category_covers", default="no-image.png")
    hidden = models.BooleanField(verbose_name="Только для избранных", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Items(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название товара")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Относится к категории:")
    price = models.IntegerField(verbose_name="Цена (в рублях)", default=0)
    weight = models.IntegerField(verbose_name="Вес", null=True, blank=True)
    description = models.TextField(verbose_name="Описание товара", null=True, blank=True)
    main_image = models.ImageField(verbose_name="Основное изображение", upload_to="item_covers", default="no-image.png")
    currency_price = models.DecimalField(verbose_name="Цена (в валюте)", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def get_currency_price(self, currency_id=1):
        self.currency_price = round(Decimal(self.price)/Currencies.objects.get(id=currency_id).exchange_rate, 2)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ItemImages(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="item_images", default="no-image.png")
    of_item = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name="Относится к товару:")
    caption = models.CharField(max_length=256, verbose_name="Подпись", null=True, blank=True)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"



