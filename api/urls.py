from django.urls import path
from .views import *

urlpatterns = [
    path('api/users/registration', UserRegistrationView.as_view()),
]