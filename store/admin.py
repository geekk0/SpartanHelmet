from django.contrib import admin
from .models import Categories, Items, ItemImages

# Register your models here.

admin.site.register(Categories)
admin.site.register(Items)
admin.site.register(ItemImages)


