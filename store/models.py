from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название категории", default="Новая категория")
    image = models.ImageField(verbose_name="Обложка", upload_to="media/category_covers", default="media/no-image.png")
    hidden = models.BooleanField(verbose_name="Только для избранных", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Items(models.Model):
    name = models.CharField(max_length=128, verbose_name="Товар", default="Новый товар")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Относится к категории:")
    price = models.IntegerField(verbose_name="Цена", default=0)
    description = models.TextField(verbose_name="Описание товара", null=True, blank=True)
    main_image = models.ImageField(verbose_name="Основное изображение", upload_to="media/item_covers", default="media/no-image.png")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ItemImages(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="media", default="no-image.png")
    of_item = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name="Относится к товару:")
    caption = models.CharField(max_length=256, verbose_name="Подпись", null=True, blank=True)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"


"""class Cart(models.Model):
    total_price = models.IntegerField(verbose_name="Общая стоимость корзины")
    total_quantity = models.IntegerField(verbose_name="Общее количество товаров в корзине")
    product = models.ManyToManyField(CartItem)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True, null=True)


class Order(models.Model):
    number = models.CharField(max_length=128, verbose_name="Номер заказа", null=True, blank=True)
    ORDER_STATUS_CHOICES = (("in processing", "in processing"), ("confirmed", "confirmed"), ("shipping", "shipping"),
                            ("delivered", "delivered"), ("cancelled", "cancelled"))
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name="Статус доставки", null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик")
    product = models.ManyToManyField('OrderItem', related_name='ordered_products')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True, null=True)"""

