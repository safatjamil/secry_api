from django.db import models
from django.contrib.auth.models import *

class User(models.Model):
    email = models.EmailField(max_length = 100)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255, null = True, blank = True)
    password = models.CharField(max_length = 300)