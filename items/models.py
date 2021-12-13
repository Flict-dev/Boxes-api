from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from Boxes.settings import ITEM_IMAGE_DIR
from django.core.cache import cache


class Item(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    description = models.TextField(max_length=3000, verbose_name='описание')
    image = models.ImageField(upload_to=ITEM_IMAGE_DIR, verbose_name='картинка')
    weight = models.PositiveIntegerField(verbose_name='вес в граммах')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена в рублях')

    class Meta:
        verbose_name = 'Коробка'
        verbose_name_plural = 'Коробки'

    def __str__(self):
        return self.title


@receiver([post_save, post_delete], sender=Item)
def invalidate_item_cache(sender, instance, **kwargs):
    from items.views import ITEM_CACHE_KEY
    cache.delete(ITEM_CACHE_KEY)
