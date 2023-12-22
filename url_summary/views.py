import os
from django.http import JsonResponse
import readtime
import google.generativeai as genai
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

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
            summary = get_article_summary(url)
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
            summary = get_video_summary(url)
            context = {"result": summary, "video_form": VideoURLForm()}
        else:
            context = {"video_form": form}

        context["article_form"] = ArticleURLForm()
        return render(request, "url_summary/video.html", context=context)
    else:
        return redirect("url_summary:home")


def get_article_summary(url):
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
    short_summary = summarize_with_gpt(article_text, source="article")
    # short_summary = summarize_with_gemini(article_text, source="article")

    # save results to DB to retrieve later if a URL is requested again
    summary_obj = URLSummary.objects.create(
        url=url, title=title, summary=short_summary, text=article_text
    )
    summary_dict = get_summary_details(summary_obj)
    return summary_dict


def get_video_summary(url):
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
    short_summary = summarize_with_gpt(formatted_transcript, source="video")
    # short_summary = summarize_with_gemini(formatted_transcript, source="video")

    response, error = download_page(url)
    if error or response.status_code != 200:
        title = "https://www.youtube.com/watch?v=" + video_id
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text

    # save results to DB to retrieve later if a URL is requested again
    summary_obj = URLSummary.objects.create(
        url=url, title=title, summary=short_summary, text=formatted_transcript
    )
    summary_dict = get_summary_details(summary_obj)
    return summary_dict


def get_summary_details(summary_obj: URLSummary) -> dict:
    """
    Generate dictionary with summary details.
    """
    result = {}
    read_time = readtime.of_text(summary_obj.text).minutes
    short_summary = summary_obj.summary
    # format summary into list of sentences for readability
    sentences = [s.strip() for s in short_summary.split("- ") if s.strip()]

    result["sentences"] = sentences
    result["title"] = summary_obj.title
    result["read_time"] = read_time
    result["url"] = summary_obj.url
    result["summary"] = summary_obj

    return result


def summarize_with_gpt(text: str, sentence_count: int = 5, source: str = "text") -> str:
    """
    Summarize text into short sentences using GPT-3.5 model.
    """
    text = text[:14000]

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # prompt = (
    #     "Summarize the following text into {sentence_count} short sentences.\n\n"
    #     'Text: """{text}""". List each sentence in bullet points.'
    # )

    prompt = (
        "In just {sentence_count} sentences, capture the heart of the {source} below. "
        "Highlight what it's about, who it's for, and why it might be interesting.\n\n"
        "Text: {text}. List each sentence in bullet points."
    )
    prompt = prompt.format(text=text, sentence_count=sentence_count, source=source)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        seed=34267,
    )
    summary = completion.choices[0].message.content
    return summary


def summarize_with_gemini(text: str, sentence_count: int = 5, source: str = "text"):
    """
    Summarize text into short sentences using Gemini Pro model.
    """
    text = text[:14000]

    prompt = (
        "In just {sentence_count} sentences, capture the heart of the {source} below. "
        "Highlight what it's about, who it's for, and why it might be interesting.\n\n"
        "Text: {text}. List each sentence in bullet points."
    )
    prompt = prompt.format(text=text, sentence_count=sentence_count, source=source)

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    summary = response.text

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
