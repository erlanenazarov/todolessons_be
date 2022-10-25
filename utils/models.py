import uuid

from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True, null=True)
