from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


@login_required
def profile(request):
    user = get_user_model().objects.get(id=request.user.id)
    bookmarks = user.bookmarked_summaries.all()
    context = {"bookmarks": bookmarks}
    return render(request, "users/profile.html", context)


@login_required
def preferences(request):
    return render(request, "users/preferences.html")


@login_required
def summary_detail(request, id):
    user = get_user_model().objects.get(id=request.user.id)
    bookmark = get_object_or_404(user.bookmarked_summaries, id=id)
    sentences = [s.strip() for s in bookmark.summary.split("- ") if s.strip()]
    context = {"bookmark": bookmark, "sentences": sentences}
    return render(request, "users/summary_detail.html", context)
