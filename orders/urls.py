from django.urls import path
from . import views


urlpatterns = [
    path("", views.order_create, name='order_create'),
    path("account_details", views.account_details, name="account_details"),
    path("edit_account_details", views.edit_account_details, name="edit_account_details")
]