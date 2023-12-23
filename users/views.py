from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Preference
from .forms import PreferenceForm


@login_required
def profile(request):
    user = get_user_model().objects.get(id=request.user.id)
    bookmarks = user.bookmarked_summaries.all()
    context = {"bookmarks": bookmarks}
    return render(request, "users/profile.html", context)


@login_required
def preferences(request):
    user_prefrence = Preference.objects.filter(user=request.user).first()
    if user_prefrence:
        context = {
            "model_choice": user_prefrence.model_choice,
            "sentence_length": user_prefrence.sentence_length,
        }
    else:
        context = {"model_choice": "gpt-3.5-turbo", "sentence_length": 5}
    return render(request, "users/preferences.html", context)


@login_required
def preference_update(request):
    if request.method == "POST":
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preference, _ = Preference.objects.get_or_create(user=request.user)
            preference.model_choice = form.cleaned_data["model_choice"]
            preference.sentence_length = form.cleaned_data["sentence_length"]
            preference.save()
            return redirect("users:preferences")
    else:
        form = PreferenceForm()

    context = {"form": form}
    return render(request, "users/preferences_form.html", context)


@login_required
def summary_detail(request, id):
    user = get_user_model().objects.get(id=request.user.id)
    bookmark = get_object_or_404(user.bookmarked_summaries, id=id)
    sentences = [s.strip() for s in bookmark.summary.split("- ") if s.strip()]
    context = {"bookmark": bookmark, "sentences": sentences}
    return render(request, "users/summary_detail.html", context)
