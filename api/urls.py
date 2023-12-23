from django.urls import path
from .views import *
from .content_views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/users/registration/", user_registration, name="user_registration"),
    path("api/users/account_details/", user_view_account, name="user_view_account"),
    path("api/users/edit_email", user_edit_email, name="user_edit_email"),
    path("api/users/edit_info", user_edit_info, name="user_edit_info"),
    path("api/users/change_password", user_change_password, name="user_change_password"),
    path("api/users/secrets/", user_edit_info, name="user_change_password"),
    path("api/secrets/create/", create_secret, name="create_secret"),
    path("api/secrets/<int:secret_id>/", user_change_password, name="user_change_password"),

]
