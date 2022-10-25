import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=False)
    username = models.TextField(max_length=255, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        name = self.get_full_name()
        if not name:
            return self.email
        return name
