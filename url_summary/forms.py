from django import forms

from .models import URLSummary


class URLInputForm(forms.ModelForm):
    class Meta:
        model = URLSummary
        fields = ("url",)

    def clean_url(self):
        url = self.cleaned_data["url"]
        if len(url) > 500:
            raise forms.ValidationError(
                "The given URL is too long. It must be 500 chars or lower."
            )
        return url
