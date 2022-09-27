import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class SneakerManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ) \
            .order_by('-id') \
            .select_related('category', 'author')


class Sneaker(models.Model):
    objects = SneakerManager()
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

    @staticmethod
    def resize_image(image, new_width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

    def save(self, *args, **kwargs):

        if not self.slug:
            slug = f'{slugify(self.title)}'
            while Sneaker.objects.filter(slug=slug).exists():
                slug = slug + '-' + get_random_string(length=4)
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved
