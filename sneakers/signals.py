import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from sneakers.models import Sneaker


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Sneaker)
def sneaker_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Sneaker.objects.filter(pk=instance.pk).first()
    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Sneaker)
def sneaker_cover_update(sender, instance, *args, **kwargs):
    old_instance = Sneaker.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    is_new_cover = old_instance != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
