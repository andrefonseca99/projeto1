from django.contrib import admin

from .models import Category, Sneaker

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Sneaker)


class SneakerAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
