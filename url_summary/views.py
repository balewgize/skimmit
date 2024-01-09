import os
import json
from django.http import JsonResponse
import readtime
import google.generativeai as genai
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube

from users.models import Preference
from .forms import ArticleURLForm, VideoURLForm
from .models import URLSummary
from .utils.downloader import download_page


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def home(request):
    context = {"article_form": ArticleURLForm(), "video_form": VideoURLForm()}
    return render(request, "index.html", context=context)


def article_summary(request):
    if request.method == "POST":
        form = ArticleURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            if request.user.is_authenticated:
                user_preference, _ = Preference.objects.get_or_create(user=request.user)
            else:
                user_preference = None
            summary = get_article_summary(url, user_preference)
            context = {"result": summary, "article_form": ArticleURLForm()}
        else:
            context = {"article_form": form}

        context["video_form"] = VideoURLForm()
        return render(request, "url_summary/article.html", context=context)
    else:
        return redirect("url_summary:home")


def video_summary(request):
    if request.method == "POST":
        form = VideoURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            if request.user.is_authenticated:
                user_preference, _ = Preference.objects.get_or_create(user=request.user)
            else:
                user_preference = None
            summary = get_video_summary(url, user_preference)
            context = {"result": summary, "video_form": VideoURLForm()}
        else:
            context = {"video_form": form}

        context["article_form"] = ArticleURLForm()
        return render(request, "url_summary/video.html", context=context)
    else:
        return redirect("url_summary:home")


def get_article_summary(url: str, user_preference: Preference):
    """
    Summarize articles by extracting HTML body text.
    """
    summary_obj = URLSummary.objects.filter(url=url).first()
    if summary_obj:
        summary_dict = get_summary_details(summary_obj)
        return summary_dict

    summary_dict = {}
    response, error = download_page(url)
    if error or response.status_code != 200:
        summary_dict["error"] = True
        return summary_dict

    soup = BeautifulSoup(response.text, "html.parser")
    article_text = soup.find("body").get_text()
    title = soup.find("title").text

    if user_preference is None:
        ai_model = "gpt-3.5-turbo"
        sentence_count = 5
    else:
        ai_model = user_preference.ai_model
        sentence_count = user_preference.sentence_count

    if ai_model == "gpt-3.5-turbo":
        ai_summary = summarize_with_gpt(article_text, sentence_count, source="article")
    else:
        ai_summary = summarize_with_gemini(
            article_text, sentence_count, source="article"
        )

    if not ai_summary:
        summary_dict["error"] = True
        return summary_dict

    # save results to DB to retrieve later if a URL is requested again
    summary_obj = URLSummary.objects.create(
        url=url,
        title=title,
        summary=ai_summary,
        text=article_text,
        ai_model=ai_model,
    )
    summary_dict = get_summary_details(summary_obj)
    return summary_dict


def get_video_summary(url: str, user_preference: Preference):
    """
    Summarize YouTube videos by extracting transcript.
    """
    summary_obj = URLSummary.objects.filter(url=url).first()
    if summary_obj:
        summary_dict = get_summary_details(summary_obj)
        return summary_dict

    summary_dict = {}
    video_id = url.split("v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    if not transcript:
        summary_dict["error"] = True
        return summary_dict

    formatter = TextFormatter()
    formatted_transcript = formatter.format_transcript(transcript)

    if user_preference is None:
        ai_model = "gpt-3.5-turbo"
        sentence_count = 5
    else:
        ai_model = user_preference.ai_model
        sentence_count = user_preference.sentence_count

    if ai_model == "gpt-3.5-turbo":
        ai_summary = summarize_with_gpt(
            formatted_transcript, sentence_count, source="video"
        )
    else:
        ai_summary = summarize_with_gemini(
            formatted_transcript, sentence_count, source="video"
        )

    if not ai_summary:
        summary_dict["error"] = True
        return summary_dict

    # save results to DB to retrieve later if a URL is requested again
    summary_obj = URLSummary.objects.create(
        url=url,
        title="",  # title will be set later
        summary=ai_summary,
        text=formatted_transcript,
        ai_model=ai_model,
    )
    summary_dict = get_summary_details(summary_obj)
    return summary_dict


def get_summary_details(summary_obj: URLSummary) -> dict:
    """
    Generate dictionary with summary details.
    """
    result = {}
    url = summary_obj.url

    if "youtube.com" in url:
        yt = YouTube(url)
        read_time = yt.length // 60  # watch time in minutes
        summary_obj.title = yt.title
        summary_obj.save()
    else:
        read_time = readtime.of_text(summary_obj.text).minutes

    # format summary into list of sentences for readability
    try:
        summary = json.loads(summary_obj.summary)
        sentences = summary["sentences"]
    except Exception as e:
        sentences = []

    result["sentences"] = sentences
    result["title"] = summary_obj.title
    result["read_time"] = read_time
    result["url"] = url
    result["summary"] = summary_obj

    return result


def summarize_with_gpt(text: str, sentence_count: int = 5, source: str = "text") -> str:
    """
    Summarize text into short sentences using GPT-3.5 model.
    """

    text = text[:14000]
    prompt = (
        "In just {sentence_count} sentences, capture the heart of the {source} text below. "
        "Highlight what it's about, who it's for, and why it might be interesting. "
        "Respond with a JSON object having the following keys: 'status': a boolean value, "
        "'title': title of the {source}, 'sentences': array of sentences."
        "The length of the 'sentences' array must be  {sentence_count} and respond "
        "with a JSON object only without any additional text.\n\n"
        'TEXT: """{text}"""'
    )
    prompt = prompt.format(text=text, sentence_count=sentence_count, source=source)

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            seed=34267,
        )
        summary = completion.choices[0].message.content
    except Exception as e:
        print(e)  # TODO: add logging
        summary = None
    return summary


def summarize_with_gemini(text: str, sentence_count: int = 5, source: str = "text"):
    """
    Summarize text into short sentences using Gemini Pro model.
    """
    text = text[:14000]
    prompt = (
        "In just {sentence_count} sentences, capture the heart of the {source} text below. "
        "Highlight what it's about, who it's for, and why it might be interesting."
        "Respond with a JSON object having the following keys: 'status': a boolean value, "
        "'title': title of the {source}, 'sentences': array of sentences."
        "The length of the 'sentences' array must be  {sentence_count} and respond "
        "with a JSON object only without any additional text.\n\n"
        'TEXT: """{text}"""'
    )
    prompt = prompt.format(text=text, sentence_count=sentence_count, source=source)

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        summary = response.text
        # returns unnecessary text sometimes
        summary = summary.replace("```JSON", "").replace("```json", "")
        summary = summary.replace("```", "")
    except Exception as e:
        print(e)  # TODO: add logging
        summary = None
    return summary


@login_required
@require_POST
def bookmark_summary(request):
    """
    Add or remove summary from user's bookmarks.
    """
    summary_id = request.POST.get("id")
    action = request.POST.get("action")
    if summary_id and action:
        try:
            summary = get_object_or_404(URLSummary, id=summary_id)
            if action == "save":
                summary.bookmarks.add(request.user)
            else:
                summary.bookmarks.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "error"})
