import os
import readtime
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
from django.views.generic import View
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from .forms import ArticleURLForm, VideoURLForm
from .models import URLSummary
from .utils.downloader import download_page


def home(request):
    context = {"article_form": ArticleURLForm(), "video_form": VideoURLForm()}
    return render(request, "index.html", context=context)


def article_summary(request):
    if request.method == "POST":
        form = ArticleURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            summary = get_article_summary(url)
            context = {"summary": summary, "article_form": ArticleURLForm()}
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
            context = {"summary": summary, "video_form": VideoURLForm()}
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
    short_summary = summarize_with_gpt(article_text)

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
    short_summary = summarize_with_gpt(formatted_transcript)

    # save results to DB to retrieve later if a URL is requested again
    summary_obj = URLSummary.objects.create(
        url=url, summary=short_summary, text=formatted_transcript
    )
    summary_dict = get_summary_details(summary_obj)
    return summary_dict


def get_summary_details(summary_obj: URLSummary) -> dict:
    """
    Generate dictionary with summary details.
    """
    summary = {}
    read_time = readtime.of_text(summary_obj.text).minutes
    short_summary = summary_obj.summary
    # format summary into list of sentences for readability
    sentences = [s.strip() for s in short_summary.split("- ") if s.strip()]

    summary["sentences"] = sentences
    summary["title"] = summary_obj.title
    summary["read_time"] = read_time
    summary["url"] = summary_obj.url

    return summary


def summarize_with_gpt(text: str, sentence_count: int = 5) -> str:
    """
    Summarize text into short sentences using GPT-3.5 model.
    """
    # TODO: preprocess text for better results
    text = text[:14000]

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the following text into {sentence_count} short sentences.\n\n"
        'Text: """{text}""". List each sentence in bullet points.'
    )
    prompt = prompt.format(text=text, sentence_count=sentence_count)

    # TODO: handle api call failure, if any
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        seed=34267,
    )
    summary = completion.choices[0].message.content
    return summary
