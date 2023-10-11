from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Recipe


@receiver(pre_delete, sender=Recipe)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.storage.delete(instance.image.name)
