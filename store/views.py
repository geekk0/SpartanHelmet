from django.shortcuts import render
from .models import Categories, Items, ItemImages
from django.views.generic import View
from .forms import LoginForm, RegistrationForm
from cart.forms import CartAddProductForm
from .forms import NewCategoryForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def signup_view(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)

    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


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


def get_available_categories(request):

    if request.user.groups.filter(name="Весь контент"):

        return Categories.objects.all().order_by("name")

    else:

        return Categories.objects.filter(hidden=False).order_by("name")


def showcase(request):

    available_categories = get_available_categories(request)

    context = {"available_categories": available_categories}

    return render(request, "showcase.html", context)


def add_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data["image"])
            form.save()

        return HttpResponseRedirect("Showcase")
    else:
        form = NewCategoryForm

        return render(request, "add_category.html", {"form": form})


def remove_category(request, category_name):
    category_to_delete = Categories.objects.get(name=category_name)
    category_to_delete.delete()

    return HttpResponseRedirect("/Showcase")


def category_items(request, category_name):

    available_categories = get_available_categories(request)

    category_object = Categories.objects.get(name=category_name)

    if category_object not in available_categories:

        raise Http404

    else:

        category_items = Items.objects.filter(category__name=category_name)

        context = {"category_items": category_items, "category_object": category_object, "category_name": category_name}

        return render(request, "category_items.html", context)


def item_page(request, category_name, item_name):

    if not Categories.objects.get(name=category_name) in get_available_categories(request):

        raise Http404

    else:

        item = Items.objects.get(name=item_name)

        images = ItemImages.objects.filter(of_item_id=item.id)

        # request.session["foo"] = "bar"

        cart_product_form = CartAddProductForm()

        context = {"item": item, "images": images, "cart_product_form": cart_product_form}


        return render(request, "item_page.html", context)