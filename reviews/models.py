from django.db import models
from django.utils import timezone

from users.models import User


class Reviews(models.Model):
    class StatusChoices(models.TextChoices):
        ON_MODERATION = 'на модерации'
        PUBLISHED = 'опубликован'
        REJECTED = 'отклонен'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', related_name='review_author')
    text = models.TextField(max_length=2000, verbose_name='текст отзыва')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания')
    published_at = models.DateTimeField(verbose_name='Дата публикации', null=True)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ON_MODERATION, max_length=30)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв номер - {self.pk}"

    def clean(self):
        if self.status == self.StatusChoices.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super(Reviews, self).clean()
