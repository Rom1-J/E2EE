from django.urls import path

from chat.pages.views import HomeView

app_name = "pages"
urlpatterns = [
    path("", view=HomeView.as_view(), name="home"),
]
