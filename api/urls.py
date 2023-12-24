from django.urls import path
from . import views
from . import content_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/users/registration/", views.user_registration, name="user_registration"),
    path("api/users/authentication/", views.user_authentication, name="user_authentication"),
    path("api/users/account_details/", views.user_view_account, name="user_view_account"),
    path("api/users/edit_email/", views.user_edit_email, name="user_edit_email"),
    path("api/users/edit_info/", views.user_edit_info, name="user_edit_info"),
    path("api/users/change_password/", views.user_change_password, name="user_change_password"),
    path("api/users/delete/", views.delete_user, name="delete_user"),

    path("api/users/secrets/", content_views.user_view_secrets, name="user_view_secrets"),
    path("api/secrets/create/", content_views.create_secret, name="create_secret"),
    path("api/secrets/<int:secret_id>/", content_views.secret_details, name="secret_details"),
    path("api/secrets/<int:secret_id>/edit/", content_views.edit_secret, name="edit_secret"),
    path("api/secrets/<int:secret_id>/delete/", content_views.delete_secret, name="delete_secret"),

]
