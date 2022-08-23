from django.contrib import admin

from .models import Category, Sneaker

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'sneaker_description'
    list_filter = 'category', 'author', 'is_published', \
        'sneaker_description_is_html'
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)
