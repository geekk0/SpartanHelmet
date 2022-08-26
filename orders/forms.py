from django import forms
from .models import Order, UserInfo
from phonenumber_field.formfields import PhoneNumberField


class OrderCreateForm(forms.ModelForm):
    phone = PhoneNumberField()
    save_info = forms.BooleanField

    def get_save_info_value(self):
        save_info = self.save_info
        print("value in form:" + str(save_info))
        return save_info

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code', 'phone']


class UserInfoUpdateForm(forms.ModelForm):
    phone = PhoneNumberField()

    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code', 'phone']

