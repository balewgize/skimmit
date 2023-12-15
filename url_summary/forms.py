from django import forms


class ArticleURLForm(forms.Form):
    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "type": "url",
                "class": "form-control",
                "placeholder": "Enter URL",
                "required": True,
                "autofocus": True,
                "maxlength": 500,
            }
        ),
    )

    def clean_url(self):
        url = self.cleaned_data["url"]
        if "www.youtube.com" in url:
            raise forms.ValidationError("Invalid Article URL.")
        return url


class VideoURLForm(forms.Form):
    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "type": "url",
                "class": "form-control",
                "placeholder": "Enter YouTube Video URL",
                "required": True,
                "autofocus": True,
                "maxlength": 100,
            }
        ),
    )

    def clean_url(self):
        try:
            url = self.cleaned_data["url"]
            if not url.startswith("https://www.youtube.com/watch?v="):
                raise

            # there may be other parameters in the URL
            video_id = url.split("v=")[1].split("&")[0]
            if len(video_id) != 11:
                raise
        except:
            video_id = None

        if not video_id:
            raise forms.ValidationError("Invalid YouTube URL.")
        return url
