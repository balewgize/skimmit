from django.urls import include, path

from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("preferences/", views.preferences, name="preferences"),
    path("summary/<int:id>/", views.summary_detail, name="summary_detail"),
]
