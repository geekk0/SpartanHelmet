from django.db import models
from store.models import Items, Categories
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(default="user_firstname", max_length=50)
    last_name = models.CharField(default="user_lastname", max_length=50)
    email = models.EmailField()
    status = models.CharField(default="Processing", max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    phone_number = PhoneNumberField(unique=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Items, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(default="user_firstname", max_length=50)
    last_name = models.CharField(default="user_lastname", max_length=50)
    email = models.EmailField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = PhoneNumberField(unique=False, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
        # self.first_name + " " + self.last_name + " " + str(self.id)

    class Meta:
        verbose_name = "User info"
        verbose_name_plural = "Users info"
