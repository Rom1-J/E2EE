from django.contrib.auth.decorators import login_required
from django.urls import path

from chat.pages.views import HomeView, AboutView

app_name = "pages"
urlpatterns = [
    path("", view=login_required(HomeView.as_view()), name="home"),
    path("about/", view=login_required(AboutView.as_view()), name="about"),
]
