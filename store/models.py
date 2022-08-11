from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название категории", default="Новая категория")
    image = models.ImageField(verbose_name="Обложка", upload_to="media/category_covers", default="media/no-image.png")

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


