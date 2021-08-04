from django.urls import path

from chat.guild.views import (
    user_detail_view,
)

app_name = "guild"

urlpatterns = [
    path("<int>/", view=user_detail_view, name="index"),
]
