from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class UserManager(BaseUserManager):

#     def _create_user(self, email, password, **extra_fields):
#         try:
#                 user = self.model(email=email, **extra_fields)
#                 user.set_password(password)
#                 user.save(using=self._db)
#                 return user
#         except:
#             return False

#     def create_user(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null = True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


# class User(models.Model):
#     email = models.EmailField(max_length = 100)
#     first_name = models.CharField(max_length = 255)
#     last_name = models.CharField(max_length = 255, null = True, blank = True)
#     password = models.BinaryField(max_length = 300)

#     @classmethod
#     def create(cls, dict_):
#         user = cls(email = dict_["email"], first_name = dict_["first_name"], last_name = dict_["first_name"], password = dict_["password"])
#         return user