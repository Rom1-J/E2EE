from django.urls import path

from .views import (
    UserClientUpdateView,
    UserDetailView,
    UserFistConnectView,
    UserRedirectView,
    UserResetPasswordView,
    UserUpdateView,
)

app_name = "users"
urlpatterns = [
    path(
        "~first_connect/",
        view=UserFistConnectView.as_view(),
        name="first_connect",
    ),
    path(
        "~first_connect/<str:page>",
        view=UserFistConnectView.as_view(),
        name="first_connect",
    ),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("~update/", view=UserUpdateView.as_view(), name="update"),
    path(
        "~update/client",
        view=UserClientUpdateView.as_view(),
        name="update_client",
    ),
    path("~security/", view=UserUpdateView.as_view(), name="security"),
    path(
        "reset_password/",
        view=UserResetPasswordView.as_view(),
        name="reset_password",
    ),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
]
