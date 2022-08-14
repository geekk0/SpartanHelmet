from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.cart_detail, name='cart_detail'),
    path("add/<int:product_id>", views.cart_add, name='cart_add'),
    path("remove/<int:product_id>", views.cart_remove, name='cart_remove'),
    path("plus_one/<int:product_id>/<int:quantity>", views.cart_plus_one, name="plus_one"),
    path("minus_one/<int:product_id>/<int:quantity>", views.cart_minus_one, name="minus_one"),

]