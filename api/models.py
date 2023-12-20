from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class User(AbstractBaseUser):

    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null = True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
