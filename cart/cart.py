from decimal import Decimal
from django.conf import settings
from store.models import Categories, Items
from currencies.models import Currencies


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'currency_price': str(product.currency_price), 'weight': str(product.weight)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def plus_one(self, product, quantity, update_quantity=False):

        product_id = str(product.id)

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def minus_one(self, product, quantity, update_quantity=False):

        product_id = str(product.id)

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def get_cart_weight(self):
        """
        Подсчет веса товаров в корзине.
        """
        return sum(Decimal(item['weight']) * item['quantity'] for item in
            self.cart.values())

    def get_shipping_value(self):

        exchange_rate = Currencies.objects.get(id=1).exchange_rate

        return round((sum(Decimal(item['weight']) * item['quantity'] * 3 for item in
                   self.cart.values()) + 750) / exchange_rate, 2)

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Items.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
            product.get_currency_price()
            product.save()

        for item in self.cart.values():
            item['currency_price'] = Decimal(item['currency_price'])
            item['weight'] = Decimal(item['weight'])
            item['total_currency_price'] = item['currency_price'] * item['quantity']
            item['total_weight'] = item['weight'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        print(sum(Decimal(item['currency_price']) * item['quantity'] for item in
                   self.cart.values()) + self.get_shipping_value())

        return sum(Decimal(item['currency_price']) * item['quantity'] for item in
                   self.cart.values()) + self.get_shipping_value()

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True