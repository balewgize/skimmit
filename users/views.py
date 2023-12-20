from django.shortcuts import render


def profile(request):
    return render(request, "users/profile.html")


def preferences(request):
    return render(request, "users/preferences.html")
