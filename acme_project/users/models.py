from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """Пользователь сайта."""

    bio = models.TextField('Боиграфия', blank=True)
