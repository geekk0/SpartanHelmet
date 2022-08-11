from django.shortcuts import render
from .models import Categories, Items, ItemImages
from django.views.generic import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse


class LoginView(View):

    def get(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        context = {'form': form}

        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        next_page = request.POST.get('next')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                return HttpResponseRedirect(next_page)

        return render(request, 'login.html', {'form': form})


def user_logout(request):
    request.user.set_unusable_password()
    logout(request)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def main_page(request):

    previous_url = (request.META.get('HTTP_REFERER'))

    if previous_url:

        context = {"previous_url": previous_url}

    else:

        context = {}

    return render(request, "main_page.html", context)


def who_we_are(request):

    context = {}

    return render(request, "who_we_are.html", context)


def showcase(request):

    categories_list = Categories.objects.all().order_by("name")

    context = {"categories_list": categories_list}

    return render(request, "showcase.html", context)


def category_items(request, category_name):

    category_items = Items.objects.filter(category__name=category_name)

    context = {"category_items": category_items, "category_name": category_name}

    return render(request, "category_items.html", context)


def item_page(request, category_name, item_name):

    item = Items.objects.get(name=item_name)

    images = ItemImages.objects.filter(of_item_id=item.id)

    context = {"item": item, "images": images}

    return render(request, "item_page.html", context)