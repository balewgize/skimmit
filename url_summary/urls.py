from django.urls import path

from . import views


app_name = "url_summary"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
]
