from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Sneaker(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    condition_value = models.IntegerField()
    condition_unit = models.CharField(default='/10', max_length=65)
    price = models.IntegerField()
    price_unit = models.CharField(default='R$', max_length=65)
    sneaker_description = models.TextField()
    sneaker_description_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='sneakers/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category, default=1, on_delete=models.SET_NULL, null=True)  # noqa: E501
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sneakers:sneaker', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            while Sneaker.objects.filter(slug=slug).exists():
                slug = slug + '-' + get_random_string(length=4)
            self.slug = slug

        return super().save(*args, **kwargs)
