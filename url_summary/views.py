import os
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic import View
from openai import OpenAI
import readtime

from .utils import download_page
from .forms import URLInputForm
from .models import URLSummary


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        form = URLInputForm()
        return render(request, "index.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        input_form = URLInputForm(request.POST)
        if input_form.is_valid():
            url = input_form.cleaned_data["url"]
            summary = self.get_summary(url)
            context = {"summary": summary, "form": URLInputForm()}
            return render(request, "index.html", context=context)

    def get_summary(self, url) -> dict:
        """Summary of a given URL from DB or generated from its page source"""
        summary_obj = URLSummary.objects.filter(url=url).first()
        if summary_obj:
            summary_dict = self.get_summary_details(summary_obj)
            return summary_dict

        summary_dict = {}
        response, error = download_page(url)
        if error or response.status_code != 200:
            summary_dict["error"] = True
            return summary_dict

        soup = BeautifulSoup(response.text, "html.parser")
        article_text = soup.find("body").get_text()
        title = soup.find("title").text
        gpt_summary = self.summarize_with_gpt(article_text)

        # save results to DB to retrieve later if a URL is requested again
        summary_obj = URLSummary.objects.create(
            url=url, title=title, summary=gpt_summary, text=article_text
        )
        summary_dict = self.get_summary_details(summary_obj)
        return summary_dict

    def get_summary_details(self, summary_obj: URLSummary) -> dict:
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

    def summarize_with_gpt(self, text: str, sentence_count: int = 5) -> str:
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
