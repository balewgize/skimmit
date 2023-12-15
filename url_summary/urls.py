from django.urls import path

from . import views


app_name = "url_summary"

urlpatterns = [
    path("", views.home, name="home"),
    path("article/", views.article_summary, name="article"),
    path("video/", views.video_summary, name="video"),
]
