from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
   email = models.EmailField(max_length = 100, unique = True)
   first_name = models.CharField(max_length = 15, null=False)
   last_name = models.CharField(max_length = 15, null=True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username', 'first_name',]
#    def __str__(self):
#        return "{}".format(self.email)
