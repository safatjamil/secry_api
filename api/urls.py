from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("api/users/registration/", user_registration, name="user_registration"),
    path("api/users/login/", user_login, name="user_login"),
    path("api/users/edit/", user_edit, name="user_edit"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]