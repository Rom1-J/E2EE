from django.urls import path

from chat.users.views import (
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
    path("~security/", view=UserUpdateView.as_view(), name="security"),
    path(
        "reset_password/",
        view=UserResetPasswordView.as_view(),
        name="reset_password",
    ),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
]
