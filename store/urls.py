from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main_page, name=""),
    path("Login", views.LoginView.as_view(), name="Login"),
    path("Logout", views.user_logout, name="Logout"),
    path("Register", views.signup_view, name="Register"),
    path("Who we are", views.who_we_are, name="Who we are"),
    path("Showcase", views.showcase, name="Showcase"),
    path("add_category", views.add_category, name="add_category"),
    path("remove_category/<str:category_name>", views.remove_category, name="remove_category"),
    path("<str:category_name>", views.category_items, name="Category items"),
    path("<str:category_name>/<str:item_name>", views.item_page, name="Item page"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)