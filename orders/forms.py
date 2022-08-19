from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField


class OrderCreateForm(forms.ModelForm):
    phone = PhoneNumberField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code', 'phone']
