from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Categories, Items, ItemImages
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'{username} user not registered')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Invalid password')

        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):

    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class NewCategoryForm(forms.ModelForm):

    hidden = forms.BooleanField(widget=forms.CheckboxInput, required=None)

    class Meta:
        model = Categories
        fields = ('name', 'image', 'hidden')


class NewItemForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = ('name', 'price', 'description', 'main_image')


class AddItemImagesForm(forms.ModelForm):
    class Meta:
        model = ItemImages
        fields = ("image", "caption")


