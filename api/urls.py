from django.urls import path
from .views import *

urlpatterns = [
    path('api/users/registration', user_registration, name = "user_registration"),
]